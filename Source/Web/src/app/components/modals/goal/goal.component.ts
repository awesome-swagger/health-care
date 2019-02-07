import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';

@Component({
  selector: 'app-goal',
  templateUrl: './goal.component.html',
  styleUrls: ['./goal.component.scss'],
})
export class GoalComponent implements OnInit {

  public data = null;

  public nameInput = '';
  public descriptionInput = '';
  public focusInput = '';
  public startDayInput = 0;
  public durationChoice = 0;
  public weeksInput = 1;
  public progress = null;

  constructor(
    private modals: ModalService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
    if (this.data && this.data.goalTemplate) {
      let g = this.data.goalTemplate;
      this.nameInput = g.name;
      this.descriptionInput = g.description;
      this.focusInput = g.focus;
      this.startDayInput = g.start_on_day;
      this.durationChoice = g.duration_weeks !== -1 ? 1 : 0;
      this.weeksInput = g.duration_weeks !== -1 ? g.duration_weeks : 1;
    } else if (this.data && this.data.mockGoal) {
      let g = this.data.mockGoal;
      this.nameInput = g.name;
      this.descriptionInput = g.description;
      this.focusInput = g.focus;
      this.progress = g.progress;
    }
  }

  public setProgress(num) {
    this.progress = num;
  }

  public clickClose() {
    this.modals.close(null);
  }

  public clickSave() {
    let durationWeeks = 0;
    switch(this.durationChoice) {
      case 0:
        durationWeeks = -1;
        break;
      case 1:
        durationWeeks = this.weeksInput;
        break;
    }
    if (this.startDayInput < 0) {
      this.startDayInput = 0;
    }
    let returnData = {
      name: this.nameInput,
      description: this.descriptionInput,
      focus: this.focusInput,
      start_on_day: this.startDayInput,
      duration_weeks: durationWeeks,
    };
    if (this.progress) {
      returnData['progress'] = this.progress;
    }
    this.modals.close(returnData);
  }
}
