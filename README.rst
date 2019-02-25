exttr
=====

|PyPI| |Pythons| |Travis| |GitHub|

Integrating extra metadata into attr.ib()

.. |PyPI| image:: https://img.shields.io/pypi/v/exttr.svg
   :alt: PyPI version
   :target: https://pypi.org/project/exttr/

.. |Pythons| image:: https://img.shields.io/pypi/pyversions/exttr.svg
   :alt: supported Python versions
   :target: https://pypi.org/project/exttr/

.. |Travis| image:: https://travis-ci.org/altendky/exttr.svg?branch=master
   :alt: Travis build status
   :target: https://travis-ci.org/altendky/exttr

.. |GitHub| image:: https://img.shields.io/github/last-commit/altendky/exttr/master.svg
   :alt: source on GitHub
   :target: https://github.com/altendky/exttr


Example
-------

With a little luck a better example will be provided later but for now, here's something.

A dev in ``#python`` was interested in having click_ build them attrs_-defined configuration objects.
Here's a basic solution for that with the click options being defined on the attrs class attributes via a custom exttr keyword argument ``click=``.

.. _attrs: https://github.com/python-attrs/attrs
.. _click: https://github.com/pallets/click

.. code-block:: python

    import collections
    import sys

    import attr
    import click
    import exttr


    exttr.register_keywords(
        exttr.Keyword(name='click'),
    )


    @attr.s
    class Configuration:
        foo = exttr.ib(click=click.option('--red'))


    def main(configuration):
        print(configuration)

    def clicked_fields(cls):
        fields = collections.OrderedDict()

        for field in attr.fields(cls):
            decorator = exttr.get(cls, field.name, 'click')

            if decorator is None:
                continue

            fields[field.name] = decorator

        return fields


    def build_click(f, cls, command_or_group):
        fields = clicked_fields(cls)

        def cli(*args, **kwargs):
            configuration = cls(*args, **kwargs)

            return f(configuration)

        for name, decorator in reversed(fields.items()):
            before = getattr(cli, '__click_params__', [])

            cli = decorator(cli)

            after = getattr(cli, '__click_params__', [])
            new = after[len(before):]

            if len(new) == 1:
                new, = new
                new.name = name

        return command_or_group(cli)


    click_main = build_click(
        f=main,
        cls=Configuration,
        command_or_group=click.command(),
    )


    sys.argv[1:] = ['--red', 'burgundy']
    try:
        click_main()
    except SystemExit:
        pass

Output:

.. code-block:: python

    Configuration(foo='burgundy')
