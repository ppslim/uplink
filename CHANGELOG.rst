Changelog
*********

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_, and this project adheres to the
`Semantic Versioning`_ scheme.

0.4.0_ - 2018-2-10
==================
Added
-----
- Support for Basic Authentication.
- The ``response_handler`` decorator for defining custom response handlers.
- The ``error_handler`` decorator for defining custom error handlers.
- The ``inject`` decorator for injecting other kinds of middleware.
- The ``Consumer._inject`` method for adding middleware to a consumer
  instance.
- Support for annotating constructor arguments of a ``Consumer`` subclass
  with built-in function annotations like ``Query`` and ``Header``.

0.3.0_ - 2018-1-09
==================
Added
-----
- HTTP HEAD request decorator by `@brandonio21`_.
- Support for returning deserialized response objects using ``marshmallow``
  schemas.
- Constructor parameter for ``Query`` and ``QueryMap`` to
  support already encoded URL parameters.
- Support for using ``requests.Session`` and ``aiohttp.ClientSession``
  instances with the ``client`` parameter of the ``Consumer``
  constructor.

Changed
-------
- ``aiohttp`` and ``twisted`` are now optional dependencies/extras.

Fixed
-----
- Fix for calling a request method with ``super``, by `@brandonio21`_.
- Fix issue where method decorators would incorrectly decorate inherited
  request methods.

0.2.2_ - 2017-11-23
===================
Fixed
-----
- Fix for error raised when an object that is not a class is passed into the
  ``client`` parameter of the ``Consumer`` constructor, by `@kadrach`_.

0.2.0_ - 2017-11-03
===================
Added
-----
- The class ``uplink.Consumer`` by `@itstehkman`_. Consumer classes should
  inherit this base.
  class, and creating consumer instances happens through instantiation.
- Support for ``asyncio`` for Python 3.4 and above.
- Support for ``twisted`` for all supported Python versions.

Changed
-------
- **BREAKING**: Invoking a consumer method now builds and executes the request,
  removing the extra step of calling the ``execute`` method.

Deprecated
----------
- Building consumer instances with ``uplink.build``. Instead, Consumer classes
  should inherit ``uplink.Consumer``.

Fixed
-----
- Header link for version 0.1.1 in changelog.

0.1.1_ - 2017-10-21
===================
Added
-----
- Contribution guide, ``CONTRIBUTING.rst``.
- "Contributing" Section in README.rst that links to contribution guide.
- ``AUTHORS.rst`` file for listing project contributors.
- Adopt `Contributor Covenant Code of Conduct`_.

.. _`Contributor Covenant Code of Conduct`: https://www.contributor-covenant.org/version/1/4/code-of-conduct.html

Changed
-------
- Replaced tentative contributing instructions in preview notice on
  documentation homepage with link to contribution guide.

0.1.0 - 2017-10-19
==================
Added
-----
- Python ports for almost all method and argument annotations in Retrofit_.
- Adherence to the variation of the semantic versioning scheme outlined in
  the official Python package distribution tutorial.
- MIT License
- Documentation with introduction, instructions for installing, and quick
  getting started guide covering the builder and all method and argument
  annotations.
- README that contains GitHub API v3 example, installation instructions with
  ``pip``, and link to online documentation.

.. General Links
.. _Retrofit: http://square.github.io/retrofit/
.. _`Keep a Changelog`: http://keepachangelog.com/en/1.0.0/
.. _`Semantic Versioning`: https://packaging.python.org/tutorials/distributing-packages/#semantic-versioning-preferred

.. Releases
.. _0.4.0: https://github.com/prkumar/uplink/compare/v0.3.0...v0.4.0
.. _0.3.0: https://github.com/prkumar/uplink/compare/v0.2.2...v0.3.0
.. _0.2.2: https://github.com/prkumar/uplink/compare/v0.2.0...v0.2.2
.. _0.2.0: https://github.com/prkumar/uplink/compare/v0.1.1...v0.2.0
.. _0.1.1: https://github.com/prkumar/uplink/compare/v0.1.0...v0.1.1

.. Contributors
.. _@brandonio21: https://github.com/brandonio21
.. _@itstehkman: https://github.com/itstehkman
.. _@kadrach: https://github.com/kadrach
