import inspect
import sys


class UnsupportedPythonVersion(Exception):
    @classmethod
    def build(cls, supported, found):
        return cls(
            'Python major version {found} not one of: {supported}'.format(
                found=found, supported=', '.join(str(v) for v in supported)
            )
        )


py = {
    major: (major, 0) <= sys.version_info < (major + 1, 0) for major in (2, 3)
}

if not any(py.values()):
    raise UnsupportedPythonVersion.build(
        supported=py.keys(), found=sys.version_info[0]
    )


if py[2]:

    def get_parameter_names(f):
        return inspect.getargspec(f).args


elif py[3]:

    def get_parameter_names(f):
        return list(inspect.signature(f).parameters.keys())
