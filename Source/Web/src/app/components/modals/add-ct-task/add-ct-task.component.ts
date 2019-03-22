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
  ];

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.totalPatients = this.data.totalPatients ? this.data.totalPatients : 0;
      this.getTaskType().dataModel.readListPaged().subscribe(
        (tasks) => {
          if (this.getTaskType().type === 'manager') {
            this.tasks = tasks.filter((obj) => obj.is_manager_task);
          } else {
            this.tasks = tasks.filter((obj) => !obj.is_manager_task);
          }
          this.tasksShown = _uniqBy(this.tasks, (obj) => {
            return obj.name;
          });
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

  public uniqByNameCount(task) {
    return this.tasks.filter((obj) => obj.name === task.name).length;
  }

  public updateTaskName(task) {
    let tasks = this.tasks.filter((obj) => obj.name === task.origName || obj.name === task.name);
    console.log(tasks);
    tasks.forEach((obj) => {
      let updateSub = this.getTaskType().dataModel.update(obj.id, {
        name: task.name,
      }, true).subscribe(
        (resp) => {
          obj.name = task.name;
          task.edit = false;
        },
        (err) => {},
        () => {
          updateSub.unsubscribe();
        }
      );
    });
  }

  public filterTasks() {
    let taskMatches = this.tasks.filter((obj) => {
      return obj.name.toLowerCase().indexOf(this.searchInput.toLowerCase()) >= 0;
    });
    this.tasksShown = _uniqBy(taskMatches, (obj) => obj.name);
  }

  public addTask(taskName) {
    if (taskName.length <= 0) {
      return;
    }
    let task = {
      start_on_day: 0,
      appear_time: '00:00:00',
      due_time: '00:00:00',
      name: taskName,
      plan_template: this.data.planTemplateId,
      category: 'interaction',
      is_manager_task: false,
    }
    if (this.getTaskType().type === 'manager') {
      task.is_manager_task = true;
    }
    let createSub = this.getTaskType().dataModel.create(task).subscribe(
      (resp) => {
        this.tasks.push(resp);
        this.createTask = false;
        this.modal.close(resp);
      },
      (err) => {},
      () => {
        createSub.unsubscribe();
      }
    );
  }

  public next(task) {
    let newTask = {
      start_on_day: 0,
      appear_time: '00:00:00',
      due_time: '00:00:00',
      name: task.name,
      plan_template: this.data.planTemplateId,
      category: 'interaction',
      is_manager_task: false,
    };
    if (this.getTaskType().type === 'manager') {
      newTask.is_manager_task = true;
    }
    let createSub = this.getTaskType().dataModel.create(newTask).subscribe(
      (resp) => {
        this.tasks.push(resp);
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
