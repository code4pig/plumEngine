#include "common/CNewTickMgr.h"
#include "common/CNewTick.h"
#include "common/log.h"

namespace common
{
	CNewTickMgr::CNewTickMgr( uint32 uTickCyc )
		:m_uCurrentTime(0)
		,m_uTickInterval( uTickCyc )
	{
		// initialize tick lists
		for( uint32 i = 0; i < TVN_SIZE; ++i )
		{
			INIT_LIST_HEAD(tv2.vec + i);
			INIT_LIST_HEAD(tv3.vec + i);
			INIT_LIST_HEAD(tv4.vec + i);
			INIT_LIST_HEAD(tv5.vec + i);
		}

		for( uint32 i = 0; i < TVR_SIZE; ++i )
			INIT_LIST_HEAD(tv1.vec + i);
	}

	void CNewTickMgr::ClearTickList(struct list_head* phead)
	{
		struct list_head *iter, *tmp;
		//遍历给定的列表，从上面把TICKSLOT都删除掉（释放内存）
		list_for_each_safe(iter, tmp, phead)
		{
			stTickEntry * pEntry = list_entry( iter, stTickEntry, TickListHead );
			if( pEntry->bIsValid )
			{
				CNewTick* pTick = pEntry->pTick;
				if( pTick != NULL )
					pTick->m_pTickEntry = NULL;
			}
			pEntry->Release();
		}
	}

	CNewTickMgr::~CNewTickMgr()
	{
		//遍历所有的tick列表，删除所有TICKSLOT对象
		int i;
		for(i=0; i<TVR_SIZE; ++i)
			ClearTickList(tv1.vec + i);
		for(i=0; i<TVN_SIZE;++i)
		{
			ClearTickList(tv2.vec + i);
			ClearTickList(tv3.vec + i);
			ClearTickList(tv4.vec + i);
			ClearTickList(tv5.vec + i);
		}

	}

	uint32 CNewTickMgr::Cascade(struct tvec *tv, int index)
	{
		/* cascade all the timers from tv up one level */
		struct list_head tv_list;

		list_replace_init(tv->vec + index, &tv_list);

		/*
		* We are removing _all_ timers from the list, so we
		* don't have to detach them individually.
		*/
		struct list_head *iter, *tmp;
		list_for_each_safe(iter, tmp, &tv_list)
		{
			stTickEntry* pEntry = list_entry(iter, stTickEntry, TickListHead );
			if( pEntry->bIsValid )
				InternalRegister( pEntry );
			else
				pEntry->Release();
		}

		return index;
	}

	void CNewTickMgr::TickStep()
	{
		struct list_head work_list;
		struct list_head *head = &work_list;
		uint32 index = (uint32)( m_uCurrentTime & TVR_MASK);

		/*
		* Cascade timers:
		*/
		if (!index && (!Cascade(&tv2, INDEX(0))) && (!Cascade(&tv3, INDEX(1))) && !Cascade(&tv4, INDEX(2)))
			Cascade(&tv5, INDEX(3));

		list_replace_init(tv1.vec + index, &work_list);
		struct list_head *iter, *tmp;
		list_for_each_safe(iter, tmp, head)
		{
			stTickEntry* pEntry = list_entry(iter, stTickEntry, TickListHead);

			// PTS对应的pTick已经UnRegister，删除pts对象
			if( !pEntry->bIsValid )
			{
				pEntry->Release();
				continue;
			}

			// 触发tick回调函数
			CNewTick* pTick = pEntry->pTick;

			pTick->OnTick();

			// 没有Unregister，需要继续触发，所以将PTS触发时间更新后重新压入队列
			if( pEntry->bIsValid )
			{
				pEntry->uNextTickTime += pTick->GetInterval();
				InternalRegister( pEntry );
			}
			else	// 触发tick以后这个tick被UnRegister掉了，这个时候不重新插入队列，但是需要将tickentry删除
			{
				pEntry->Release();
			}
		}
	}

	void CNewTickMgr::OnTick()
	{
		// 每次同时触发uTickInterval这么多次
		for( uint32 i=0; i < m_uTickInterval; i++ )
		{
			TickStep();
			++ m_uCurrentTime;
		}
	}

	void CNewTickMgr::InternalRegister( stTickEntry * pTickEntry )
	{
		uint64 expires = pTickEntry->uNextTickTime;
		uint32 idx = (uint32)(expires - m_uCurrentTime);
		struct list_head *vec;

		if (idx < TVR_SIZE)
		{
			uint32 i = (uint32)(expires & TVR_MASK);
			vec = tv1.vec + i;
		}
		else if (idx < 1 << (TVR_BITS + TVN_BITS))
		{
			uint32 i = (uint32)(expires >> TVR_BITS) & TVN_MASK;
			vec = tv2.vec + i;
		}
		else if (idx < 1 << (TVR_BITS + 2 * TVN_BITS))
		{
			uint32 i = (uint32)(expires >> (TVR_BITS + TVN_BITS)) & TVN_MASK;
			vec = tv3.vec + i;
		}
		else if (idx < 1 << (TVR_BITS + 3 * TVN_BITS))
		{
			uint32 i = (uint32)(expires >> (TVR_BITS + 2 * TVN_BITS)) & TVN_MASK;
			vec = tv4.vec + i;
		}
		else
		{
			uint32 i = (uint32)(expires >> (TVR_BITS + 3 * TVN_BITS)) & TVN_MASK;
			vec = tv5.vec + i;
		}
		/*
		* Timers are FIFO:
		*/
		list_add_tail( &pTickEntry->TickListHead, vec );
	}

	bool CNewTickMgr::Register( CNewTick* pTick, uint32 uInterval, const char * szName )
	{

		if( szName == NULL )
		{
			LOG_ERROR("%s", "注册Tick失败: Tick名无效。" );
			return false;
		}
		if( uInterval == 0 )
		{
			LOG_ERROR("注册Tick(%s)失败: uInterval必须大于0。", szName);
			return false;
		}

		UnRegister(pTick);

		pTick->m_pTickMgr		= this;
		pTick->m_uInterval		= uInterval;
		pTick->SetTickName(szName);

		stTickEntry * pEntry	= stTickEntry::CreateObj();//_ArkNew(stTickEntry, "Tick stTickEntry");
		pEntry->pTick			= pTick;
		pEntry->uNextTickTime	= m_uCurrentTime + pTick->GetInterval();
		pEntry->bIsValid		= true;

		INIT_LIST_HEAD( &pEntry->TickListHead );
		pTick->m_pTickEntry = pEntry;

		InternalRegister( pEntry );		// 将TICKSLOT注册进队列

		return true;
	}

	void CNewTickMgr::UnRegister( CNewTick* pTick )
	{
		// Unregsiter的时候并不马上删除tickentry对象，而是将pTick与tickentry对象关系解除
		// tickentry对象留在之后Cascade或者OnTick的时候会被删除
		if( pTick->m_pTickMgr == this && pTick->m_pTickEntry != NULL)
		{
			pTick->m_pTickEntry->bIsValid = false;
			pTick->m_pTickEntry = NULL;
		}
	}

}
