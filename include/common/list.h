/*
Copyright (C) 2017, Zhang Baofeng.

BSD 2-Clause License (http://www.opensource.org/licenses/bsd-license.php)

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following disclaimer
in the documentation and/or other materials provided with the
distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

You can contact the author via email : zhangbaofeng@joygame.cc
This is modified from linux kernel's list implementation.
*/

#pragma once

namespace common{

	/*
		* from linux kernel
		*/

	#ifndef _LINUX_LIST_H
	#define _LINUX_LIST_H
	#pragma warning( push ) 
	#pragma warning( disable :4312)
	/*
		* poison.h
		*/
	#define LIST_POISON1  ((list_head *) 0xC0100100)
	#define LIST_POISON2  ((list_head *) 0xC0200200)

	/*
		* stddef.h
		*/
	#undef NULL
	#if defined(__cplusplus)
	#define NULL 0
	#else
	#define NULL ((void *)0)
	#endif

	#ifdef __cplusplus
	#define OFFSETOF_BASE 0x1
	#define Offsetof(TYPE, MEMBER) \
		(size_t)((unsigned char*)(&(((TYPE*)OFFSETOF_BASE)->MEMBER)) - (unsigned char*)(TYPE*)OFFSETOF_BASE)
	#else
	#define Offsetof offsetof
	#endif

	//#ifndef offsetof
	//#define offsetof(TYPE, MEMBER) ((size_t) &((TYPE *)0)->MEMBER)
	//#endif

	/*
		* Simple doubly linked list implementation.
		*
		* Some of the internal functions ("__xxx") are useful when
		* manipulating whole lists rather than single entries, as
		* sometimes we already know the next/prev entries and we can
		* generate better code by using them directly rather than
		* using the generic single-entry routines.
		*/

		struct list_head {
			struct list_head *next, *prev;
		};

	#define LIST_HEAD_INIT(name) { &(name), &(name) }

	#define LIST_HEAD(name) \
	  struct list_head name = LIST_HEAD_INIT(name)

		inline void INIT_LIST_HEAD(struct list_head *list) {
			list->next = list;
			list->prev = list;
		}

		/*
		 * Insert a new entry between two known consecutive entries.
		 *
		 * This is only for internal list manipulation where we know
		 * the prev/next entries already!
		 */
		static inline void __list_add(struct list_head *nnew,
		struct list_head *prev,
		struct list_head *next) {
			next->prev = nnew;
			nnew->next = next;
			nnew->prev = prev;
			prev->next = nnew;
		}

		/**
		 * list_add - add a new entry
		 * @new: new entry to be added
		 * @head: list head to add it after
		 *
		 * Insert a new entry after the specified head.
		 * This is good for implementing stacks.
		 */
		static inline void list_add(struct list_head *nnew, struct list_head *head) {
			__list_add(nnew, head, head->next);
		}

		/**
		 * list_add_tail - add a new entry
		 * @new: new entry to be added
		 * @head: list head to add it before
		 *
		 * Insert a new entry before the specified head.
		 * This is useful for implementing queues.
		 */
		static inline void list_add_tail(struct list_head *nnew,
		struct list_head *head) {
			__list_add(nnew, head->prev, head);
		}


		/*
		 * Delete a list entry by making the prev/next entries
		 * point to each other.
		 *
		 * This is only for internal list manipulation where we know
		 * the prev/next entries already!
		 */
		static inline void __list_del(struct list_head * prev,
		struct list_head * next) {
			next->prev = prev;
			prev->next = next;
		}

		/**
		 * list_del - deletes entry from list.
		 * @entry: the element to delete from the list.
		 * Note: list_empty on entry does not return true after this, the entry is
		 * in an undefined state.
		 */
		static inline void list_del(struct list_head *entry) {
			__list_del(entry->prev, entry->next);
			entry->next = LIST_POISON1;
			entry->prev = LIST_POISON2;
		}


		/**
		 * list_replace - replace old entry by new one
		 * @old : the element to be replaced
		 * @new : the new element to insert
		 * Note: if 'old' was empty, it will be overwritten.
		 */
		static inline void list_replace(struct list_head *old,
		struct list_head *nnew) {
			nnew->next = old->next;
			nnew->next->prev = nnew;
			nnew->prev = old->prev;
			nnew->prev->next = nnew;
		}

		static inline void list_replace_init(struct list_head *old,
		struct list_head *nnew) {
			list_replace(old, nnew);
			INIT_LIST_HEAD(old);
		}

		/**
		 * list_del_init - deletes entry from list and reinitialize it.
		 * @entry: the element to delete from the list.
		 */
		static inline void list_del_init(struct list_head *entry) {
			__list_del(entry->prev, entry->next);
			INIT_LIST_HEAD(entry);
		}

		/**
		 * list_move - delete from one list and add as another's head
		 * @list: the entry to move
		 * @head: the head that will precede our entry
		 */
		static inline void list_move(struct list_head *list, struct list_head *head) {
			__list_del(list->prev, list->next);
			list_add(list, head);
		}

		/**
		 * list_move_tail - delete from one list and add as another's tail
		 * @list: the entry to move
		 * @head: the head that will follow our entry
		 */
		static inline void list_move_tail(struct list_head *list,
		struct list_head *head) {
			__list_del(list->prev, list->next);
			list_add_tail(list, head);
		}

		/**
		 * list_is_last - tests whether @list is the last entry in list @head
		 * @list: the entry to test
		 * @head: the head of the list
		 */
		static inline int list_is_last(const struct list_head *list,
			const struct list_head *head) {
			return list->next == head;
		}

		/**
		 * list_empty - tests whether a list is empty
		 * @head: the list to test.
		 */
		static inline int list_empty(const struct list_head *head) {
			return head->next == head;
		}

		static inline void __list_splice(struct list_head *list,
		struct list_head *head) {
			struct list_head *first = list->next;
			struct list_head *last = list->prev;
			struct list_head *at = head->next;

			first->prev = head;
			head->next = first;

			last->next = at;
			at->prev = last;
		}

		/**
		 * list_splice - join two lists
		 * @list: the new list to add.
		 * @head: the place to add it in the first list.
		 */
		static inline void list_splice(struct list_head *list, struct list_head *head) {
			if (!list_empty(list))
				__list_splice(list, head);
		}

		/**
		 * list_splice_init - join two lists and reinitialise the emptied list.
		 * @list: the new list to add.
		 * @head: the place to add it in the first list.
		 *
		 * The list at @list is reinitialised
		 */
		static inline void list_splice_init(struct list_head *list,
		struct list_head *head) {
			if (!list_empty(list)) {
				__list_splice(list, head);
				INIT_LIST_HEAD(list);
			}
		}

	/**
		* list_entry - get the struct for this entry
		* @ptr:        the &struct list_head pointer.
		* @type:       the type of the struct this is embedded in.
		* @member:     the name of the list_struct within the struct.
		*/
	#define list_entry(ptr, type, member) \
			((type *)((char *)(ptr)-Offsetof(type,member)))

	/**
		* list_for_each	-	iterate over a list
		* @pos:	the &struct list_head to use as a loop cursor.
		* @head:	the head for your list.
		*/
	#define list_for_each(pos, head) \
	  for (pos = (head)->next; pos != (head); \
		  pos = pos->next)

	/**
		* __list_for_each	-	iterate over a list
		* @pos:	the &struct list_head to use as a loop cursor.
		* @head:	the head for your list.
		*
		* This variant differs from list_for_each() in that it's the
		* simplest possible list iteration code, no prefetching is done.
		* Use this for code that knows the list to be very short (empty
		* or 1 entry) most of the time.
		*/
	#define __list_for_each(pos, head) \
	  for (pos = (head)->next; pos != (head); pos = pos->next)

	/**
		* list_for_each_prev	-	iterate over a list backwards
		* @pos:	the &struct list_head to use as a loop cursor.
		* @head:	the head for your list.
		*/
	#define list_for_each_prev(pos, head) \
	  for (pos = (head)->prev; pos != (head); \
		  pos = pos->prev)

	/**
		* list_for_each_safe - iterate over a list safe against removal of list entry
		* @pos:	the &struct list_head to use as a loop cursor.
		* @n:		another &struct list_head to use as temporary storage
		* @head:	the head for your list.
		*/
	#define list_for_each_safe(pos, n, head) \
	  for (pos = (head)->next, n = pos->next; pos != (head); \
		  pos = n, n = pos->next)

	#pragma warning( pop ) 
	#endif

};