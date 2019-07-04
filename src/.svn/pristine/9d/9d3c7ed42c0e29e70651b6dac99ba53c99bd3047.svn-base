#include <stdarg.h>
#include <stdio.h>
#include "common/common.h"
#include "common/log.h"
#include "common/CLogger.h"

namespace common{

	int MyPrintf(const char *format, ...)
	{
		va_list args;
		va_start(args, format);
		char pfBuf[512] = { 0 };
		int nret = vsnprintf(pfBuf, sizeof(pfBuf) - 1, format, args);
		LOG_INFO_NOFMT(pfBuf);
		va_end(args);
		return nret;
	}

	void InitLogger(const char *pszLogDir, const char *pszAppName)
	{
		CLogger::CreateLogger(pszLogDir, pszAppName);
	}

	void UninitLogger()
	{
		CLogger::DestroyLogger();
	}


	void SetLogLevel(LogLevel logLv)
	{
		CLogger::Instance()->SetLogLevel(logLv);
	}


	int IsEnabledLogLevel(LogLevel logLv)
	{
		return (int)CLogger::Instance()->IsEnabledLevel(logLv);
	}


	void Log(LogLevel uLevel, const char* szFormat, ...)
	{
		char szLog[4096] = { 0 };

		va_list va;
		va_start(va, szFormat);
		vsnprintf(szLog, sizeof(szLog) - 1, szFormat, va);
		va_end(va);

		CLogger::Instance()->LogMod(uLevel, szLog);
	}

	void LogScriptCache(const char* szFormat, ...)
	{
		char szLog[4096] = { 0 };

		va_list va;
		va_start(va, szFormat);
		vsnprintf(szLog, sizeof(szLog) - 1, szFormat, va);
		va_end(va);
		CLogger::Instance()->ScriptCache(szLog);
	}

	void LogScriptFlush()
	{
		CLogger::Instance()->ScriptFlush(LOG_LV_INFO);
	}

	void LogMod(LogLevel uLevel, const char* szMod, const char* szFormat, ...)
	{
		char szLog[4096] = { 0 };

		va_list va;
		va_start(va, szFormat);
		vsnprintf(szLog, sizeof(szLog) - 1, szFormat, va);
		va_end(va);

		CLogger::Instance()->LogMod(uLevel, szLog, szMod);
	}


	void Log_NoFormat(LogLevel uLevel, const char *pszMsg, const char* pszMod)
	{
		CLogger::Instance()->LogMod(uLevel, pszMsg, pszMod);
	}

};
