/*
 * External kernel module dependency exemple - master module
 *
 * Copyright (C) 2020 Hubert CHAUMETTE
 */

#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/module.h>
#include <linux/mutex.h>
#include <linux/types.h>

#include "include/master.h"

#define MASTER_NAME	"master"
#define MASTER_BUF_SZ	128

static DEFINE_MUTEX(master_lock);
static BLOCKING_NOTIFIER_HEAD(master_chain_head);
static int master_major;
static struct class *master_class;
static char master_buf[MASTER_BUF_SZ] = { 0 };
static int master_count = 0;
static struct device *master_device;

int master_notifier_register(struct notifier_block *nb)
{
	return blocking_notifier_chain_register(&master_chain_head, nb);
}
EXPORT_SYMBOL(master_notifier_register);

int master_notifier_unregister(struct notifier_block *nb)
{
	return blocking_notifier_chain_unregister(&master_chain_head, nb);
}
EXPORT_SYMBOL(master_notifier_unregister);

static ssize_t master_read(struct file *fp, char __user *buf,
			   size_t count, loff_t *offset)
{
	(void)fp;

	ssize_t ret;
	size_t read_count = min(master_count - *offset, count);
	struct master_evt_data data = {
		.buf = buf,
		.count = read_count,
	};

	if (*offset >= master_count - 1)
		return 0;

	mutex_lock(&master_lock);

	if (copy_to_user(buf, master_buf + *offset, read_count)) {
		ret = -EFAULT;
		goto unlock;
	}
	*offset += read_count;
	ret = read_count;

	blocking_notifier_call_chain(&master_chain_head, MASTER_EVT_READ, &data);

unlock:
	mutex_unlock(&master_lock);

	return ret;
}

static ssize_t master_write(struct file *fp, const char __user *buf,
			    size_t count, loff_t *offset)
{
	(void)offset;
	(void)fp;

	ssize_t ret;
	struct master_evt_data data = {
		.buf = buf,
		.count = count,
	};

	if (count > MASTER_BUF_SZ)
		return -EFBIG;

	mutex_lock(&master_lock);

	if (copy_from_user(master_buf, buf, count)) {
		ret = -EFAULT;
		goto unlock;
	}
	ret = count;
	master_count = count;

	blocking_notifier_call_chain(&master_chain_head, MASTER_EVT_WRITE, &data);

unlock:
	mutex_unlock(&master_lock);

	return ret;
}

static const struct file_operations master_fops = {
	.owner =	THIS_MODULE,
	.write =	master_write,
	.read =		master_read,
	.llseek =	no_llseek,
};

static int __init master_init(void)
{
	int ret = 0;

	master_major = register_chrdev(0, MASTER_NAME, &master_fops);
	if (master_major < 0) {
		ret = master_major;
		goto err;
	}

	master_class = class_create(THIS_MODULE, MASTER_NAME);
	if (IS_ERR(master_class)) {
		ret = PTR_ERR(master_class);
		goto err_class;
	}

	master_device = device_create(master_class, NULL, MKDEV(master_major, 0),
				      NULL, MASTER_NAME);
	if (IS_ERR(master_device)) {
		ret = PTR_ERR(master_device);
		goto err_device;
	}

	return ret;

err_device:
	class_destroy(master_class);
err_class:
	unregister_chrdev(master_major, MASTER_NAME);
err:
	return ret;
}
module_init(master_init);

static void __exit master_exit(void)
{
	device_destroy(master_class, MKDEV(master_major, 0));
	class_destroy(master_class);
	unregister_chrdev(master_major, MASTER_NAME);
}
module_exit(master_exit);

MODULE_AUTHOR("Hubert CHAUMETTE");
MODULE_DESCRIPTION("External kernel module dependency exemple - master module");
MODULE_LICENSE("GPL");
