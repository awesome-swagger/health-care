import { Component, OnInit } from '@angular/core';
import {
  groupBy as _groupBy,
  uniqBy as _uniqBy,
} from 'lodash';
import { ModalService } from '../../../modules/modals';
import { StoreService } from '../../../services';

@Component({
  selector: 'app-add-ct-task',
  templateUrl: './add-ct-task.component.html',
  styleUrls: ['./add-ct-task.component.scss'],
})
export class AddCTTaskComponent implements OnInit {

  public data = null;
  public totalPatients = 0;
  public tasks = [];
  public searchInput = '';
  public tasksShown = [];
  public selectedTask = null;
  public createTask = false;

  public typeChoices = [
    {
      type: 'manager',
      title: 'Add CM Task',
      dataModel: this.store.TeamTaskTemplate,
    },
    {
      type: 'team',
      title: 'Add CT Task',
      dataModel: this.store.TeamTaskTemplate,
    },
    {
      type: 'patient',
      title: 'Add Patient Task',
      dataModel: this.store.PatientTaskTemplate,
    },
    {
      type: 'symptom',
      title: 'Add Symptom Task',
      dataModel: this.store.SymptomTaskTemplate,
    },
    {
      type: 'plan-patient',
      title: 'Add Patient Task',
      dataModel: this.store.PatientTaskTemplate,
      relatedModel: this.store.PlanPatientTemplate,
    }
  ];

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.totalPatients = this.data.totalPatients ? this.data.totalPatients : 0;
      this.getTaskType().dataModel.readListPaged({
        is_available: true,
      }).subscribe(
        (tasks) => {
          if (this.getTaskType().type === 'manager') {
            this.tasks = tasks.filter((obj) => obj.is_manager_task);
          } else {
            this.tasks = tasks.filter((obj) => !obj.is_manager_task);
          }
          this.tasksShown = _uniqBy(this.tasks, (obj) => this.getTaskName(obj));
          console.log(this.tasksShown);
        },
        (err) => {},
        () => {}
      );
    }
  }

  public getTaskType() {
    if (!this.data || !this.data.type) {
      return this.typeChoices[0];
    } else {
      return this.typeChoices.find((obj) => obj.type === this.data.type);
    }
  }

  public isSinglePlan() {
    let type = this.getTaskType().type;
    let singlePlanTypes = ['plan-patient'];
    return singlePlanTypes.includes(type);
  }

  public getTaskName(task) {
    return task.name;
  }

  public getTaskNameRelated(task) {
    if (!this.isSinglePlan()) {
      return task.name;
    } else {
      return task.patient_task_template.name;
    }
  }

  public filterTasks() {
    let taskMatches = this.tasks.filter((obj) => {
      return this.getTaskName(obj).toLowerCase().indexOf(this.searchInput.toLowerCase()) >= 0;
    });
    this.tasksShown = _uniqBy(taskMatches, (obj) => {
      return this.getTaskName(obj);
    });
  }

  public selectTask(task) {
    if (task.delete || task.edit) {
      return;
    }
    this.selectedTask = task;
  }

  public uniqByNameCount(task) {
    let tasks = this.tasks.filter(
      (obj) => {
        return this.getTaskName(obj) === this.getTaskName(task);
      }
    )
    if (!this.isSinglePlan()) {
      tasks = tasks.filter(
        (obj) => obj.is_active === true
      );
    }
    return tasks.length;
  }

  public clickEditTask(task, e) {
    e.stopPropagation();
    task.edit = !task.edit;
    task.origName = task.name;
  }

  public clickUndoName(task, e) {
    e.stopPropagation();
    task.edit = !task.edit;
    task.name = task.origName;
  }

  public updateTaskName(task, e) {
    e.stopPropagation();
    let tasks = this.tasks.filter((obj) => obj.name === task.origName || obj.name === task.name);
    tasks.forEach((obj) => {
      let updateSub = this.getTaskType().dataModel.update(obj.id, {
        name: task.name,
      }, true).subscribe(
        (resp) => {
          obj.name = task.name;
          task.edit = false;
          this.tasksShown = _uniqBy(this.tasks, (obj) => {
            return obj.name;
          });
        },
        (err) => {},
        () => {
          updateSub.unsubscribe();
        }
      );
    });
  }

  public clickDeleteTask(task, e) {
    e.stopPropagation();
    task.delete = true;
  }

  public clickUndoDelete(task, e) {
    e.stopPropagation();
    task.delete = false;
  }

  public confirmDeleteTask(task, e) {
    e.stopPropagation();
    let tasks = this.tasks.filter((obj) => obj.name === task.origName || obj.name === task.name);
    tasks.forEach((obj) => {
      let updateSub = this.getTaskType().dataModel.update(obj.id, {
        is_available: false,
        is_active: false
      }, true).subscribe(
        (resp) => {
          let index = this.tasks.findIndex((a) => a.id === resp.id);
          this.tasks.splice(index, 1);
          task.delete = false;
          this.tasksShown = _uniqBy(this.tasks, (obj) => {
            return obj.name;
          });
        },
        (err) => {},
        () => {
          updateSub.unsubscribe();
        }
      );
    });
  }

  public addTask(taskName) {
    if (taskName.length <= 0) {
      return;
    }
    let task = {};
    if (!this.isSinglePlan()) {
      task = {
        start_on_day: 0,
        appear_time: '00:00:00',
        due_time: '00:00:00',
        name: taskName,
        plan_template: this.data.planTemplateId,
        is_manager_task: false,
      };
      if (this.getTaskType().type === 'team' || this.getTaskType().type === 'manager') {
        task['category'] = 'interaction';
      }
      if (this.getTaskType().type === 'manager') {
        task['is_manager_task'] = true;
      }
    } else {
      task = {
        custom_start_on_day: 0,
        custom_appear_time: '00:00:00',
        custom_due_time: '00:00:00',
        plan: this.data.planId,
      };
    }
    if (!this.isSinglePlan) {
      let createSub = this.getTaskType().dataModel.create(task).subscribe(
        (resp) => {
          this.tasks.push(resp);
          this.tasksShown = _uniqBy(this.tasks, (obj) => {
            return obj.name;
          });
          this.createTask = false;
          this.modal.close(resp);
        },
        (err) => {},
        () => {
          createSub.unsubscribe();
        }
      );
    } else {
      let createSub = this.getTaskType().relatedModel.create(task).subscribe(
        (resp) => {
          this.createTask = false;
          this.modal.close(resp);
        },
        (err) => {},
        () => {
          createSub.unsubscribe();
        }
      );
    }
  }

  public next(task) {
    let newTask = {
      start_on_day: 0,
      appear_time: '00:00:00',
      due_time: '00:00:00',
      name: task.name,
      plan_template: this.data.planTemplateId,
      is_manager_task: false,
    };
    if (this.getTaskType().type === 'symptom') {
      newTask['default_symptoms'] = task.default_symptoms.map((obj) => obj.id);
    }
    if (this.getTaskType().type === 'team' || this.getTaskType().type === 'manager') {
      newTask['category'] = 'interaction';
    }
    if (this.getTaskType().type === 'manager') {
      newTask['is_manager_task'] = true;
    }
    let createSub = this.getTaskType().dataModel.create(newTask).subscribe(
      (resp) => {
        this.tasks.push(resp);
        this.tasksShown = _uniqBy(this.tasks, (obj) => {
          return obj.name;
        });
        this.createTask = false;
        this.modal.close(resp);
      },
      (err) => {},
      () => {
        createSub.unsubscribe();
      }
    );
  }

  public close() {
    this.modal.close(null);
  }
}
