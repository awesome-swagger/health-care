import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';
import { FormGroup,FormControl } from '@angular/forms';
import { ERROR_COLLECTOR_TOKEN } from '@angular/platform-browser-dynamic/src/compiler_factory';
import { StoreService } from '../../../services';



@Component({
  selector: 'app-edit-task',
  templateUrl: './edit-task.component.html',
  styleUrls: ['./edit-task.component.scss'],
})
export class EditTaskComponent implements OnInit {

  public data = null;
  public frequencyOptions: Array<any> = [
    {displayName: 'Daily', value: 'daily'},
    {displayName: 'Weekly', value: 'weekly'},
    {displayName: 'Other', value: 'other'},  
  ];
  public task;
  public taskForm:FormGroup;


  constructor(    
    private modal: ModalService,
    private store: StoreService
  ) {

  }

  public ngOnInit() {

    this.initForm(this.data);
    this.task = this.data;
    this.data = this.data || {};
  }

  public close() {
    this.modal.close(null);
  }

  public initForm(data) {
    data = data || {};
    this.taskForm = new FormGroup({
      appear_time: new FormControl(data.appear_time),
      category: new FormControl(data.category),
      due_time: new FormControl(data.due_time),
      frequency: new FormControl(data.frequency),
      is_manager_task: new FormControl(data.is_manager_task),
      name: new FormControl(data.name),
      plan_template: new FormControl(data.plan_template),
      repeat_amount_input: new FormControl(data.repeat_amount >=0? data.repeat_amount: 0),
      repeat_amount: new FormControl(data.repeat_amount),
      role: new FormControl(data.role),
      start_on_day: new FormControl(data.start_on_day)
    });
  }
  public updateTaskName(task) {
    this.store.TeamTaskTemplate.update(task.id,task).subscribe((resp)=> {
       console.log(resp);
    });

  }
  public submitTask() {
    let keys = Object.keys(this.task);
    keys.forEach((key) => {
     if (this.taskForm.value[key] != undefined) {
        if(key === 'repeat_amount' && this.taskForm.value['repeat_amount'] != -1){
          this.task[key] = this.taskForm.value['repeat_amount_input'];
        }
        else {
          this.task[key] = this.taskForm.value[key];
        }
      }
    });
    this.store.TeamTaskTemplate.update(this.task.id, this.task).subscribe((r) => {
      this.modal.close(r);
    })
 
 
  }
}
