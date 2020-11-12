import re
import typing as t

from frozendict import frozendict
from rich.console import Console
import valideer as V

from pipe.core.exceptions import PipeException, StepExecutionException, StepValidationException


class Step:
    """
    Abstract class providing interface for all steps related classes

    There are three types of steps:

    Extractor, Loader, Transformer.

    *How to understand which one you need:*

    1. If you need to get data (**extract**) from **external** source, you need extractor
    2. If you need to send data (**load**) to **external** source, you need loader
    3. If you need to interact with data (**transform**) you need transformer
    """
    _available_methods = ('extract', 'transform', 'load')
    required_fields = None

    def __and__(self, other):

        def run(self, store: frozendict):

            try:
                result_a = self.obj_a.run(store)
                result_b = self.obj_b.run(store)
            except Exception:
                return store

            return store.copy(**dict(obj_a=result_a, obj_b=result_b))

        return Step.factory(run, 'AndStep', obj_a=self, obj_b=other)()

    def __or__(self, other):

        def run(self, store: frozendict):

            try:
                result = self.obj_a.run(store)
            except Exception as e:
                store = store.copy(exception=e)
                result = self.obj_b.run(store)

            return result

        return Step.factory(run, 'OrStep', obj_a=self, obj_b=other)()

    def _parse_dynamic_fields(self) -> t.NoReturn:
        dynamic_config = {}

        for key in self.required_fields.keys():
            if (key.startswith('+{') or key.startswith('{')) and key.endswith('}'):
                variable_name = re.match(r'^+?{([a-z_A-Z])+\}$', key).pop()
                dynamic_config.update({
                    getattr(self, variable_name): self.required_fields.get(key)
                })
                del self.required_fields[key]

        self.required_fields = dict(**self.required_fields, **dynamic_config)

    def validate(self, store: frozendict) -> frozendict:
        self._parse_dynamic_fields()

        validator = V.parse(self.required_fields)
        try:
            adapted = validator.validate(store)
        except V.ValidationError as e:
            raise StepValidationException(
                f'Validation for step {self.__class__.__name__} failed with error \n{e.message}')

        return store.copy(**adapted)

    @classmethod
    def factory(cls, run_method, name='', **kwargs):
        return type(name, (cls,), dict(run=run_method, **kwargs))

    def run(self, store: frozendict) -> frozendict:
        """
        Method which provide ability to run any step.

        Pipe shouldn't know which exactly step is
        running, that's why we need run method. But developers should be limited in 3 options,
        which presented in `_available_methods`

        You can extend this class and change `_available_methods` field, if you want to customize
        this behavior

        :param store: Current pipe state
        :return: frozendict
        """

        if self.required_fields is not None:
            store = self.validate(store)

        for method in self._available_methods:
            if hasattr(self, method):
                return getattr(self, method)(store)

        raise StepExecutionException(
            f"You should define one of this methods - {','.join(self._available_methods)}")


# Base classes for semantics and behavior control

class Extractor(Step):
    pass


class Transformer(Step):
    pass


class Loader(Step):
    pass


class BasePipe:
    """
    Base class for all pipes, implements running logic and inspection of pipe state on every
    step
    """

    # Flag which show, should pipe print its state every step
    __inspection_mode: bool

    def __init__(self, initial, inspection: bool = False):
        self.__inspection_mode = inspection
        self.store = self.before_pipe(frozendict(initial))

    def set_inspection(self, enable: bool = True):
        """
        Sets inspection mode

        Examples:

        *Toggle inspection on*::

        >>> MyPipe({}).set_inspection()

        *Toggle inspection off*::

        >>> MyPipe({}).set_inspection(False)

        :param enable:
        :return: None
        """
        self.__inspection_mode = enable

    def __print_step(self, step: Step, store: frozendict):
        """
        Prints passed step and store to the console

        :param step:
        :param store:
        :return: None
        """
        console = Console()

        console.log('Current step is -> ', step.__class__.__name__, f'({step.__module__})')
        console.log(f'{step.__class__.__name__} STORE STATE')
        console.log('----------------------------------------------------------------')
        console.log(store)
        console.log('----------------------------------------------------------------')
        console.log('\n\n')

    def _run_pipe(self, pipe: t.Iterable[Step]) -> t.Union[None, t.Any]:
        """
        Protected method to run subpipe declared in schema (schema can be different depending on
        pipe type)

        :param pipe:
        :return: Pipe result
        """

        for item in pipe:

            if self.__inspection_mode:
                self.__print_step(item, self.store)

            if issubclass(item.__class__, Extractor) or issubclass(item.__class__, Transformer):
                intermediate_store = item.run(self.store)

                if self.interrupt(intermediate_store):
                    return self.after_pipe(intermediate_store)

                if intermediate_store is None or not issubclass(frozendict,
                                                                intermediate_store.__class__):
                    raise PipeException(
                        'Transformer and Extractor should always return a frozendict')  #
                    # noqa: E501
                else:
                    self.store = intermediate_store

            if issubclass(item.__class__, Loader):
                intermediate_store = item.run(self.store)

                if issubclass(intermediate_store.__class__, frozendict) or isinstance(
                        intermediate_store, frozendict):
                    self.store = intermediate_store

        return self.after_pipe(self.store)

    def before_pipe(self, store: frozendict) -> frozendict:
        """
        Hook for running custom pipe (or anything) before every pipe execution

        :param store:
        :return: None
        """
        return store

    def after_pipe(self, store: frozendict) -> frozendict:
        """
        Hook for running custom pipe (or anything) after every pipe execution

        :param store:
        :return: None
        """
        return store

    def interrupt(self, store: frozendict) -> bool:
        """
        Interruption hook which could be overridden, allow all subclassed pipes set one
        condition, which will
        be respected after any step was run. If method returns true, pipe will not be finished and will
        return value returned by step immediately (respect after_pipe hook)

        :param store:
        :return: bool
        """
        return False

    def __str__(self) -> str:
        return self.__class__.__name__


class NamedPipe(BasePipe):
    """
    Simple pipe structure to interact with named pipes.

    Example::

    >>> class MyPipe(NamedPipe):
    ...     pipe_schema = {
    ...         'crop_image': (EImage('<path>'), TCropImage(width=230, height=140), LSaveImage(
    '<path>'))
    ...     }
    ...
    ...image_path = MyPipe(<initial_store>).run_pipe('crop_image')

    """
    pipe_schema: t.Dict[str, t.Iterable[Step]]

    def run_pipe(self, name: str):
        pipe_to_run = self.pipe_schema.get(name, ())
        return self._run_pipe(pipe_to_run)