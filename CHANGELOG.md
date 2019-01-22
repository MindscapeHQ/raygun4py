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
