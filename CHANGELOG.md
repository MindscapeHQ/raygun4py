## 4.1.0 (01/11/2018):
Bugfix:
  - Fix request building in WSGI middlewares that had not been updated to use the new improved WSGI request handling, thanks for noticing @ericb-granular ([#73](https://github.com/MindscapeHQ/raygun4py/pull/73))

## 4.0.0 (31/10/2018):
Breaking changes:
  - Support for Python 2.6 has been dropped

Features:
  - Improved WSGI request request handling, Thanks @ericb-granular ([#70](https://github.com/MindscapeHQ/raygun4py/pull/70))
