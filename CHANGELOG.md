# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [0.2.1] - 2023-02-28

### Added

### Changed

### Fixed

- Fixed the docstring for `store.search` in the stub file to show right annotations for `skip` and `limit`

## [0.2.0] - 2023-01-16

### Added

### Changed

- Changed the `Store()` and `AsyncStore()` signatures, replacing `max_index_key_len` option with `is_search_enabled`.
- Permanently set the maximum index key length to 3
- Changed benchmarks to compare operations when search is enabled to when search is disabled.

### Fixed

## [0.1.1] - 2023-01-14

### Added

### Changed

- Updated the stub file for the `search()` method.

### Fixed

## [0.1.0] - 2023-01-12

### Added

- Added full-text search for keys, with pagination using `store.search(term, skip, limit)`

### Changed

- Changed the `Store::new()` signature to include `max_search_index_key_length` option.

### Fixed

## [0.0.3] - 2022-11-09

### Added

### Changed

### Fixed

- A Few Typos (including those in the upstream rust package scdb)

## [0.0.2] - 2022-10-28

### Added

### Changed

### Fixed

- A Few Typos (including those in the upstream rust package scdb)

## [0.0.1] - 2022-10-28

### Added

- Initial release

### Changed

### Fixed
