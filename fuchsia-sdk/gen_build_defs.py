#!/usr/bin/env python
# Copyright 2018 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# Generates a single BUILD.gn file with build targets generated using the
# manifest files in the SDK.

import json
import os
import subprocess
import sys


# Inserted at the top of the generated BUILD.gn file.
_GENERATED_PREAMBLE = """# DO NOT EDIT! This file was generated by
# //third_party/fuchsia-sdk/gen_build_defs.py.
# Any changes made to this file will be discarded.

import("//third_party/fuchsia-sdk/fuchsia_sdk_pkg.gni")

"""

def SerializeListOfStrings(strings):
  """Outputs a list of strings in GN-friendly, double-quoted format."""

  return '[' + ','.join(['"{}"'.format(s) for s in strings]) + ']'

def ReformatTargetName(dep_name):
  """Removes the namespace from |target| and substitutes invalid target
  characters with valid ones (e.g. hyphens become underscores)."""

  assert not '.' in dep_name, "Invalid target name: %s" % dep_name
  reformatted_name = dep_name.replace('-','_')
  return reformatted_name

def ConvertCommonFields(json):
  """Extracts fields from JSON manifest data which are used across all
  target types. Note that FIDL packages do their own processing."""

  return {
    'target_name': ReformatTargetName(json['name']),
    'public_deps': [':' + ReformatTargetName(dep) for dep in json['deps']]
  }

def FormatGNTarget(fields):
  """Returns a GN target definition as a string.

  |fields|: The GN fields to include in the target body.
            'target_name' and 'type' are mandatory."""

  output = '%s("%s") {\n' % (fields['type'], fields['target_name'])
  del fields['target_name']
  del fields['type']

  for key, val in fields.iteritems():
    if isinstance(val, str) or isinstance(val, unicode):
      val_serialized = '\"%s\"' % val
    elif isinstance(val, list):
      # Serialize a list of strings in the prettiest possible manner.
      if len(val) == 0:
        val_serialized = '[]'
      elif len(val) == 1:
        val_serialized = '[ \"%s\" ]' % val[0]
      else:
        val_serialized = '[\n    ' + ',\n    '.join(
            ['\"%s\"' % x for x in val]) + '\n  ]'
    else:
      raise Exception('Could not serialize %r' % val)

    output += '  %s = %s\n' % (key, val_serialized)
  output += '}'

  return output

def ReformatFidlTargetName(dep_name):
  """Converts a FIDL |dep_name| consisting of dot-delimited namespaces, and
  package name, to a single underscore delimited name."""

  assert not '-' in dep_name, "Invalid FIDL target name: %s" % dep_name

  # For convenience, treat "fuchsia.*" namespace as top-level.
  if dep_name[:8] == 'fuchsia.':
    dep_name = dep_name[8:]

  reformatted_name = dep_name.replace('.','_')
  return reformatted_name

def ConvertFidlLibrary(json):
  """Converts a fidl_library manifest entry to a GN target.

  Arguments:
    json: The parsed manifest JSON.
  Returns:
    The GN target definition, represented as a string."""

  converted = {
      'public_deps': [
          ':' + ReformatFidlTargetName(dep) for dep in json['deps']],
      'sources': json['sources'],
      'target_name': ReformatFidlTargetName(json['name']),
      'type': 'fuchsia_sdk_fidl_pkg'
  }

  # Override the package name & namespace, otherwise the rule will generate
  # a top-level package with |target_name| as its directory name.
  name_parts = json['name'].split('.')
  converted['package_name'] = name_parts[-1]
  converted['namespace'] = '.'.join(name_parts[:-1])

  return converted

def ConvertCcPrebuiltLibrary(json):
  """Converts a cc_prebuilt_library manifest entry to a GN target.

  Arguments:
    json: The parsed manifest JSON.
  Returns:
    The GN target definition, represented as a string."""

  converted = ConvertCommonFields(json)
  converted['type'] = 'fuchsia_sdk_pkg'
  converted['sources'] = json['headers']
  converted['include_dirs'] = [json['root'] + '/include']

  if json['format'] == 'shared':
    converted['shared_libs'] = [json['name']]
  else:
    converted['static_libs'] = [json['name']]

  return converted

def ConvertCcSourceLibrary(json):
  """Converts a cc_source_library manifest entry to a GN target.

  Arguments:
    json: The parsed manifest JSON.
  Returns:
    The GN target definition, represented as a string."""

  converted = ConvertCommonFields(json)
  converted['type'] = 'fuchsia_sdk_pkg'

  # Headers and source file paths can be scattered across "sources", "headers",
  # and "files". Merge them together into one source list.
  converted['sources'] = json['sources']
  if 'headers' in json:
    converted['sources'] += json['headers']
  if 'files' in json:
    converted['sources'] += json['files']
  converted['sources'] = list(set(converted['sources']))

  converted['include_dirs'] = [json['root'] + '/include']
  converted['public_deps'] += \
      [':' + ReformatFidlTargetName(dep) for dep in json['fidl_deps']]

  return converted

def ConvertNoOp(json):
  """Null implementation of a conversion function. No output is generated."""

  return None


"""Maps manifest types to conversion functions."""
_CONVERSION_FUNCTION_MAP = {
  'fidl_library': ConvertFidlLibrary,
  'cc_source_library': ConvertCcSourceLibrary,
  'cc_prebuilt_library': ConvertCcPrebuiltLibrary,

  # No need to build targets for these types yet.
  'dart_library': ConvertNoOp,
  'host_tool': ConvertNoOp,
  'image': ConvertNoOp,
  'loadable_module': ConvertNoOp,
  'sysroot': ConvertNoOp,
  'documentation': ConvertNoOp,
}


def ConvertSdkManifests():
  sdk_base_dir = os.path.join(os.path.dirname(__file__), 'sdk')
  toplevel_meta = json.load(open(os.path.join(sdk_base_dir, 'meta',
                                              'manifest.json')))

  build_output_path = os.path.join(sdk_base_dir, 'BUILD.gn')
  with open(build_output_path, 'w') as buildfile:
    buildfile.write(_GENERATED_PREAMBLE)

    for part in toplevel_meta['parts']:
      parsed = json.load(open(os.path.join(sdk_base_dir, part['meta'])))

      convert_function = _CONVERSION_FUNCTION_MAP.get(part['type'])
      if convert_function is None:
        raise Exception('Unexpected SDK artifact type %s in %s.' %
                        (parsed['type'], next_part))

      converted = convert_function(parsed)
      if converted:
        buildfile.write(FormatGNTarget(converted) + '\n\n')


if __name__ == '__main__':
  sys.exit(ConvertSdkManifests())
