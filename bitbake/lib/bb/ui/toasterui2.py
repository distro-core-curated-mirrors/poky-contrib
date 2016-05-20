from uuid import uuid4
from datetime import datetime

_evt_list = [
    "bb.build.TaskBase",
    "bb.build.TaskFailed",
    "bb.build.TaskFailedSilent",
    "bb.build.TaskStarted",
    "bb.build.TaskSucceeded",
    "bb.command.CommandCompleted",
    "bb.command.CommandExit",
    "bb.command.CommandFailed",
    "bb.cooker.CookerExit",
    "bb.event.BuildCompleted",
    "bb.event.BuildStarted",
    "bb.event.CacheLoadCompleted",
    "bb.event.CacheLoadProgress",
    "bb.event.CacheLoadStarted",
    "bb.event.ConfigParsed",
    "bb.event.DepTreeGenerated",
    "bb.event.LogExecTTY",
    "bb.event.MetadataEvent",
    "bb.event.MultipleProviders",
    "bb.event.NoProvider",
    "bb.event.ParseCompleted",
    "bb.event.ParseProgress",
    "bb.event.RecipeParsed",
    "bb.event.SanityCheck",
    "bb.event.SanityCheckPassed",
    "bb.event.TreeDataPreparationCompleted",
    "bb.event.TreeDataPreparationStarted",
    "bb.runqueue.runQueueTaskCompleted",
    "bb.runqueue.runQueueTaskFailed",
    "bb.runqueue.runQueueTaskSkipped",
    "bb.runqueue.runQueueTaskStarted",
    "bb.runqueue.sceneQueueTaskCompleted",
    "bb.runqueue.sceneQueueTaskFailed",
    "bb.runqueue.sceneQueueTaskStarted",
    "logging.LogRecord"]

"""
server: bb.server.ServerCommunicator
event_handler: ProcessEventQueue
params:

server.server is a bb.server.ProcessServer
server.server.pid is the pid for the process running this UI
server.server.command_channel is a multiprocessing.Connection
"""
def main(server, event_handler, params):
    # create a unique identifier for this instance of toasterui2;
    # this uses the datetime and is guaranteed unique
    run_id = uuid4()
    print("Unique ID for this run: %s" % run_id)

    # set event mask
    log_level, debug_domains = bb.msg.constructLogOptions()
    command_and_params = ["setEventMask",
                          server.getEventHandle(),
                          log_level,
                          debug_domains,
                          _evt_list]
    result, error = server.runCommand(command_and_params)
    if not result or error:
        print("can't set event mask: %s", error)
        return 1

    # receive events
    while True:
        try:
            event = event_handler.waitEvent(0.25)

            if event:
                # attach the run ID to the event
                event._toaster_run_id = run_id

                print(event)
        except Exception as e:
            print("exiting due to exception: %s" % e)
            return 1

    return 0