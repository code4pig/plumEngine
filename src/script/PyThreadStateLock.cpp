#include "script/PyThreadStateLock.h"

namespace script
{
	PyThreadStateLock::PyThreadStateLock(void)
	{
		state = PyGILState_Ensure();
	}

	PyThreadStateLock::~PyThreadStateLock(void)
	{
		PyGILState_Release(state);
	}
}