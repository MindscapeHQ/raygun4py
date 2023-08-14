## 4.4.0 (11/08/2023):
Features:
  - Added `RaygunHandler.from_sender()` factory to construct a `RaygunHandler` instance using an existing `RaygunSender`. This allows for additional configuration of the sender.
  - Added a `config` parameter the to Flask and WSGI middleware provider constructors. This also allows for additional configuration of the sender.
  - The `RaygunHandler` now adds tags corresponding to the logging level, which now defaults to `logging.ERROR`.
  - Errors/exceptions sent via the `RaygunHandler` now have their message overriden by the logged message.
Bug fixes:
  - The `RaygunHandler` now attempts to capture `exc_info` from the `record`. This can be obtained if `logger.exception()` is used or if `exc_info=True` is set in the logger call.
    - If `exc_info` cannot be obtained by the `RaygunHandler`, it no longer attempts to construct a `RaygunErrorMessage` with `None` values. Instead, it generates a fallback error message using information gathered from the `record`. This is essentially an error with a single stack frame representing the call to the logger.
Quality of life updates:
  - Updated `CONTRIBUTING.MD`.
  - Got unit tests running again (`django` upgrade).
  - Updated `python3/samples/sample.py` and `python3/samples/sampleWithLogging.py`.
  - Cleaned up `python3/raygun4py/cli.py`.

## 4.3.0 (06/06/2019):
Features:
  - Added a new config option, `transmit_environment_variables`, to control sending any environment variables at all
  - Added support to `filter_keys` config option for ignoring keys with a simple wildcard approach. See README for more information

## 4.2.3 (28/03/2019):
Bugfixes
  - Add request `rawData` to the `build_wsgi_compliant_request` utilities to fix a bug where `rawData` is set manually then overwritten by an empty object.

## 4.2.2 (23/01/2019):
Bugfixes
  - Fix `set_request_details` builder method not returning self causing it to be unchainable

## 4.2.1 (18/12/2018):
Bugfixes
  - Set version correctly in crash report sent to Raygun API ([#78](https://github.com/MindscapeHQ/raygun4py/pull/79))

- Improve Flash middleware ([#79](https://github.com/MindscapeHQ/raygun4py/pull/79))

Thanks to @brock for both of these changes

## 4.2.0 (03/12/2018):
BugFixes
  - Further improved WSGI request handling and fixes problems with forms and WSGI requests ([#76](https://github.com/MindscapeHQ/raygun4py/pull/76))

Thanks @ericb-granular

## 4.1.0 (01/11/2018):
Bugfix:
  - Fix request building in WSGI middlewares that had not been updated to use the new improved WSGI request handling, thanks for noticing @ericb-granular ([#73](https://github.com/MindscapeHQ/raygun4py/pull/73))

## 4.0.0 (31/10/2018):
Breaking changes:
  - Support for Python 2.6 has been dropped

Features:
  - Improved WSGI request request handling, Thanks @ericb-granular ([#70](https://github.com/MindscapeHQ/raygun4py/pull/70))

### For pre 4.0.0 changelog see CHANGELOG.old.rst
