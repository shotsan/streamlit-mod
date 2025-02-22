# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from streamlit import util


class Error(Exception):
    """The base class for all exceptions thrown by Streamlit.

    Should be used for exceptions raised due to user errors (typically via
    StreamlitAPIException) as well as exceptions raised by Streamlit's internal
    code.
    """

    pass


class CustomComponentError(Error):
    """Exceptions thrown in the custom components code path."""

    pass


class DeprecationError(Error):
    pass


class FragmentStorageKeyError(Error, KeyError):
    """A KeyError raised when a KeyError is encountered during a FragmentStorage
    operation."""

    pass


class FragmentHandledException(Exception):
    """An exception that is raised by the fragment
    when it has handled the exception itself.
    """

    pass


class NoStaticFiles(Error):
    pass


class NoSessionContext(Error):
    pass


class MarkdownFormattedException(Error):
    """Exceptions with Markdown in their description.

    Instances of this class can use markdown in their messages, which will get
    nicely formatted on the frontend.
    """

    pass


class UncaughtAppException(Error):
    """Catchall exception type for uncaught exceptions that occur during script execution."""

    def __init__(self, exc):
        self.exc = exc


class StreamlitAPIException(MarkdownFormattedException):
    """Base class for Streamlit API exceptions.

    An API exception should be thrown when user code interacts with the
    Streamlit API incorrectly. (That is, when we throw an exception as a
    result of a user's malformed `st.foo` call, it should be a
    StreamlitAPIException or subclass.)

    When displaying these exceptions on the frontend, we strip Streamlit
    entries from the stack trace so that the user doesn't see a bunch of
    noise related to Streamlit internals.

    """

    def __repr__(self) -> str:
        return util.repr_(self)


class DuplicateWidgetID(StreamlitAPIException):
    pass


class StreamlitDuplicateElementId(DuplicateWidgetID):
    """An exception raised when the auto-generated ID of an element is not unique."""

    def __init__(self, element_type: str):
        super().__init__(
            f"There are multiple `{element_type}` elements with the same "
            "auto-generated ID. When this element is created, it is assigned an "
            "internal ID based on the element type and provided parameters. Multiple "
            "elements with the same type and parameters will cause this error.\n\n"
            "To fix this error, please pass a unique `key` argument to the "
            f"`{element_type}` element."
        )


class StreamlitDuplicateElementKey(DuplicateWidgetID):
    """An exception raised when the key of an element is not unique."""

    def __init__(self, user_key: str):
        super().__init__(
            f"There are multiple elements with the same `key='{user_key}'`. "
            "To fix this, please make sure that the `key` argument is unique for "
            "each element you create."
        )


class UnserializableSessionStateError(StreamlitAPIException):
    pass


class StreamlitAPIWarning(StreamlitAPIException, Warning):
    """Used to display a warning.

    Note that this should not be "raised", but passed to st.exception
    instead.
    """

    def __init__(self, *args):
        super().__init__(*args)
        import inspect
        import traceback

        f = inspect.currentframe()
        self.tacked_on_stack = traceback.extract_stack(f)

    def __repr__(self) -> str:
        return util.repr_(self)


class StreamlitModuleNotFoundError(StreamlitAPIWarning):
    """Print a pretty message when a Streamlit command requires a dependency
    that is not one of our core dependencies."""

    def __init__(self, module_name, *args):
        message = (
            f'This Streamlit command requires module "{module_name}" to be '
            "installed."
        )
        super().__init__(message, *args)
