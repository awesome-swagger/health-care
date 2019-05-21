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
  public isAdhoc = false; // Determines if the task being added is only for a single plan
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
      type: 'plan-manager',
      title: 'Add CM Task',
      dataModel: this.store.TeamTaskTemplate,
      relatedModel: this.store.PlanTeamTemplate,
      relatedField: 'team_task_template',
    },
    {
      type: 'plan-team',
      title: 'Add CT Task',
      dataModel: this.store.TeamTaskTemplate,
      relatedModel: this.store.PlanTeamTemplate,
      relatedField: 'team_task_template',
    },
    {
      type: 'plan-patient',
      title: 'Add Patient Task',
      dataModel: this.store.PatientTaskTemplate,
      relatedModel: this.store.PlanPatientTemplate,
      relatedField: 'patient_task_template',
    },
    {
      type: 'plan-symptom',
      title: 'Add Symptom Task',
      dataModel: this.store.SymptomTaskTemplate,
      relatedModel: this.store.PlanSymptomTemplate,
      relatedField: 'symptom_task_template',
    },
  ];

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.totalPatients = this.data.totalPatients ? this.data.totalPatients : 0;
      if (this.data.planTemplateId) {
        this.isAdhoc = false;
      } else if (this.data.planId) {
        this.isAdhoc = true;
      }
      this.getTaskType().dataModel.readListPaged({
        is_available: true,
      }).subscribe(
        (tasks) => {
          this.tasks = tasks;
          let type = this.getTaskType().type;
          if (type === 'manager' || type === 'plan-manager') {
            this.tasks = this.tasks.filter((obj) => obj.is_manager_task);
          } else if (this.getTaskType().type === 'team' || type === 'plan-team') {
            this.tasks = this.tasks.filter((obj) => !obj.is_manager_task);
          }
          this.tasksShown = _uniqBy(this.tasks, (obj) => obj.name);
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

  public isTeamTask() {
    let teamTaskTypes = ['manager', 'team', 'plan-manager', 'plan-team'];
    return teamTaskTypes.includes(this.getTaskType().type);
  }

  public filterTasks() {
    let taskMatches = this.tasks.filter((obj) => {
      return obj.name.toLowerCase().indexOf(this.searchInput.toLowerCase()) >= 0;
    });
    this.tasksShown = _uniqBy(taskMatches, (obj) => {
      return obj.name;
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
        return obj.name === task.name;
      }
    ).filter((obj) => obj.is_active === true);
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
    if (!this.isAdhoc) {
      task = {
        start_on_day: 0,
        frequency: 'once',
        repeat_amount: -1,
        appear_time: '00:00:00',
        due_time: '00:00:00',
        is_active: true,
        is_available: true,
        plan_template: this.data.planTemplateId,
        name: taskName,
        is_manager_task: false,
      };
      if (this.getTaskType().type === 'team' || this.getTaskType().type === 'manager') {
        task['category'] = 'interaction';
      }
      if (this.getTaskType().type === 'team') {
        task['roles'] = [];
      }
      if (this.getTaskType().type === 'manager') {
        task['is_manager_task'] = true;
      }
      this.createTask = false;
      this.modal.close(task);
    } else {
      task = {
        start_on_day: 0,
        frequency: 'once',
        repeat_amount: -1,
        appear_time: '00:00:00',
        due_time: '00:00:00',
        name: taskName,
        plan: this.data.planId,
      };
      if (this.getTaskType().type === 'plan-team' || this.getTaskType().type === 'plan-manager') {
        task['category'] = 'interaction';
      }
      if (this.getTaskType().type === 'plan-team') {
        task['roles'] = [];
      }
      if (this.getTaskType().type === 'plan-manager') {
        task['is_manager_task'] = true;
      }
      this.createTask = false;
      this.modal.close(task);
    }
  }

  public next(task) {
    let newTask = {};
    newTask = {
      start_on_day: task.start_on_day,
      frequency: task.frequency,
      repeat_amount: task.repeat_amount,
      appear_time: task.appear_time,
      due_time: task.due_time,
      name: task.name,
      is_manager_task: false,
    };
    if (!this.isAdhoc) {
      newTask['plan_template'] = this.data.planTemplateId;
    } else {
      newTask['plan'] = this.data.planId;
      newTask[this.getTaskType().relatedField] = task;
    }
    if (this.getTaskType().type === 'symptom' || this.getTaskType().type === 'plan-symptom') {
      newTask['default_symptoms'] = task.default_symptoms;
    }
    if (this.isTeamTask()) {
      newTask['category'] = 'interaction';
    }
    if (this.getTaskType().type === 'manager') {
      newTask['is_manager_task'] = true;
    }
    if (this.getTaskType().type === 'team') {
      newTask['roles'] = [];
    }
    this.createTask = false;
    this.modal.close(newTask);
  }

  public close() {
    this.modal.close(null);
  }
}
