/*
 * External kernel module dependency exemple - master module
 *
 * Copyright (C) 2020 Hubert CHAUMETTE
 */

#ifndef MASTER_H
#define MASTER_H

#include <linux/notifier.h>

enum master_evt_type {
	MASTER_EVT_READ,
	MASTER_EVT_WRITE,
};

struct master_evt_data {
	char __user *buf;
	size_t count;
};

int master_notifier_register(struct notifier_block *nb);
int master_notifier_unregister(struct notifier_block *nb);

#endif /* MASTER_H */
