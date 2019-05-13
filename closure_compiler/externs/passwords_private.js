// Copyright 2019 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// This file was generated by:
//   tools/json_schema_compiler/compiler.py.
// NOTE: The format of types has changed. 'FooType' is now
//   'chrome.passwordsPrivate.FooType'.
// Please run the closure compiler before committing changes.
// See https://chromium.googlesource.com/chromium/src/+/master/docs/closure_compilation.md

/** @fileoverview Externs generated from namespace: passwordsPrivate */

/**
 * @const
 */
chrome.passwordsPrivate = {};

/**
 * @enum {string}
 */
chrome.passwordsPrivate.ExportProgressStatus = {
  NOT_STARTED: 'NOT_STARTED',
  IN_PROGRESS: 'IN_PROGRESS',
  SUCCEEDED: 'SUCCEEDED',
  FAILED_CANCELLED: 'FAILED_CANCELLED',
  FAILED_WRITE_FAILED: 'FAILED_WRITE_FAILED',
};

/**
 * @typedef {{
 *   origin: string,
 *   shown: string,
 *   link: string
 * }}
 */
chrome.passwordsPrivate.UrlCollection;

/**
 * @typedef {{
 *   urls: !chrome.passwordsPrivate.UrlCollection,
 *   username: string,
 *   numCharactersInPassword: number,
 *   federationText: (string|undefined),
 *   id: number
 * }}
 */
chrome.passwordsPrivate.PasswordUiEntry;

/**
 * @typedef {{
 *   urls: !chrome.passwordsPrivate.UrlCollection,
 *   id: number
 * }}
 */
chrome.passwordsPrivate.ExceptionEntry;

/**
 * @typedef {{
 *   status: !chrome.passwordsPrivate.ExportProgressStatus,
 *   folderName: (string|undefined)
 * }}
 */
chrome.passwordsPrivate.PasswordExportProgress;

/**
 * Function that logs that the Passwords page was accessed from the Chrome
 * Settings WebUI.
 */
chrome.passwordsPrivate.recordPasswordsPageAccessInSettings = function() {};

/**
 * Changes the username and password corresponding to |id|.
 * @param {number} id The id for the password entry being updated.
 * @param {string} new_username The new username.
 * @param {string=} new_password The new password.
 */
chrome.passwordsPrivate.changeSavedPassword = function(
    id, new_username, new_password) {};

/**
 * Removes the saved password corresponding to |id|. If no saved password for
 * this pair exists, this function is a no-op.
 * @param {number} id The id for the password entry being removed.
 */
chrome.passwordsPrivate.removeSavedPassword = function(id) {};

/**
 * Removes the saved password exception corresponding to |exceptionUrl|. If no
 * exception with this URL exists, this function is a no-op.
 * @param {number} id The id for the exception url entry being removed.
 */
chrome.passwordsPrivate.removePasswordException = function(id) {};

/**
 * Undoes the last removal of a saved password or exception.
 */
chrome.passwordsPrivate.undoRemoveSavedPasswordOrException = function() {};

/**
 * Returns the plaintext password corresponding to |id|. Note that on some
 * operating systems, this call may result in an OS-level reauthentication. Once
 * the password has been fetched, it will be returned via |callback|.
 * @param {number} id The id for the password entry being being retrieved.
 * @param {function((string|undefined)):void} callback The callback that gets
 *     invoked with the retrieved password.
 */
chrome.passwordsPrivate.requestPlaintextPassword = function(id, callback) {};

/**
 * Returns the list of saved passwords.
 * @param {function(!Array<!chrome.passwordsPrivate.PasswordUiEntry>):void}
 *     callback Called with the list of saved passwords.
 */
chrome.passwordsPrivate.getSavedPasswordList = function(callback) {};

/**
 * Returns the list of password exceptions.
 * @param {function(!Array<!chrome.passwordsPrivate.ExceptionEntry>):void}
 *     callback Called with the list of password exceptions.
 */
chrome.passwordsPrivate.getPasswordExceptionList = function(callback) {};

/**
 * Triggers the Password Manager password import functionality.
 */
chrome.passwordsPrivate.importPasswords = function() {};

/**
 * Triggers the Password Manager password export functionality. Completion Will
 * be signaled by the onPasswordsFileExportProgress event. |callback| will be
 * called when the request is started or rejected. If rejected
 * <code>chrome.runtime.lastError</code> will be set to 'in-progress' or
 * 'reauth-failed'.
 * @param {function():void} callback
 */
chrome.passwordsPrivate.exportPasswords = function(callback) {};

/**
 * Requests the export progress status. This is the same as the last value seen
 * on the onPasswordsFileExportProgress event. This function is useful for
 * checking if an export has already been initiated from an older tab, where we
 * might have missed the original event.
 * @param {function(!chrome.passwordsPrivate.ExportProgressStatus):void}
 *     callback
 */
chrome.passwordsPrivate.requestExportProgressStatus = function(callback) {};

/**
 * Stops exporting passwords and cleans up any passwords, which were already
 * written to the filesystem.
 */
chrome.passwordsPrivate.cancelExportPasswords = function() {};

/**
 * Fired when the saved passwords list has changed, meaning that an entry has
 * been added or removed.
 * @type {!ChromeEvent}
 */
chrome.passwordsPrivate.onSavedPasswordsListChanged;

/**
 * Fired when the password exceptions list has changed, meaning that an entry
 * has been added or removed.
 * @type {!ChromeEvent}
 */
chrome.passwordsPrivate.onPasswordExceptionsListChanged;

/**
 * Fired when the status of the export has changed.
 * @type {!ChromeEvent}
 */
chrome.passwordsPrivate.onPasswordsFileExportProgress;
