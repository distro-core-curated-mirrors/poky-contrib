/*
 * External kernel module dependency exemple - slave module
 *
 * Copyright (C) 2020 Hubert CHAUMETTE
 */

#include <linux/module.h>
#include <master.h>

static int slave_notify(struct notifier_block *self,
			unsigned long action, void *data);

static struct notifier_block slave_nb = {
	.notifier_call = slave_notify,
};

static int slave_notify(struct notifier_block *self,
			unsigned long action, void *data)
{
	struct master_evt_data *d = (struct master_evt_data *)data;

	BUG_ON(data == NULL);

	switch (action) {
	case MASTER_EVT_READ:
		pr_info("slave: \"%.*s\" read from master\n", d->count, d->buf);
		break;
	case MASTER_EVT_WRITE:
		pr_info("slave: \"%.*s\" written to master\n", d->count, d->buf);
		break;
	default:
		break;
	}

	return NOTIFY_DONE;
}

static int __init slave_init(void)
{
	return master_notifier_register(&slave_nb);
}
module_init(slave_init);

static void __exit slave_exit(void)
{
	master_notifier_unregister(&slave_nb);
}
module_exit(slave_exit);

MODULE_AUTHOR("Hubert CHAUMETTE");
MODULE_DESCRIPTION("External kernel module dependency exemple - slave module");
MODULE_LICENSE("GPL");
