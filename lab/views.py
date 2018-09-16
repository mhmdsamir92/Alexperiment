from django.views.decorators.csrf import csrf_exempt
from lab.models.run import Run
from lab.models.workflow import Workflow
from lab.models.workflow_perm import WorkflowPerm
from lab.models.result import Result
from lab.tasks import execute_all_workflows
from django.http import JsonResponse
import json


@csrf_exempt
def start_alexperiment(request):
    workflows = json.loads(request.body)["workflows"]
    run = Run()
    run.save()
    execute_all_workflows.delay(workflows, run.id)
    return JsonResponse({"run_id": run.id})

@csrf_exempt
def get_run_results(request):
    run_id = request.GET["id"]
    workflows = Workflow.objects.filter(run_id=run_id)
    response_results = []
    for workflow in workflows:
        wf_res = []
        wf_perms = WorkflowPerm.objects.filter(workflow_id=workflow.id)
        for wf_perm in wf_perms:
            wf_perm_dict = {}
            wf_perm_dict["description"] = json.loads(wf_perm.description)
            res = {}
            results = Result.objects.filter(wf_perm_id=wf_perm.id, is_final_result=True)
            for result in results:
                res[result.key] = result.value
            wf_perm_dict["results"] = res
            wf_res.append(wf_perm_dict)
        response_results.append(wf_res)
    return JsonResponse({"results": response_results})
