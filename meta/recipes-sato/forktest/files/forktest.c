#include <glib.h>

static void
child_setup (gpointer user_data)
{
  g_print ("in child setup\n");
}

int
main (int argc, char **argv)
{
  GError *error = NULL;
  char *argp[] = { "touch", "/tmp/foo", NULL };

  if (!g_spawn_sync (NULL, argp, NULL,
                     G_SPAWN_SEARCH_PATH, child_setup, NULL,
                     NULL, NULL, NULL, &error)) {
    g_print ("Spawn failed: %s\n", error->message);
  } else {
    g_print ("Spawn worked\n");
  }
  return 0;
}
