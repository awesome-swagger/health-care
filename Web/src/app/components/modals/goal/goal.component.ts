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
    if (this.data && this.data.goalTemplate) {
      let g = this.data.goalTemplate;
      this.nameInput = g.name;
      this.descriptionInput = g.description;
      this.focusInput = g.focus;
      this.startDayInput = g.start_on_day;
      this.durationChoice = g.duration_weeks !== -1 ? 1 : 0;
      this.weeksInput = g.duration_weeks !== -1 ? g.duration_weeks : 1;
    } else if (this.data && this.data.goal) {
      let g = this.data.goal;
      this.nameInput = g.goal_template.name;
      this.descriptionInput = g.goal_template.description;
      this.focusInput = g.goal_template.focus;
      this.progress = g.latest_progress ? g.latest_progress.rating : 0;
    }
  }

  public setProgress(num) {
    this.progress = num;
  }

  public clickClose() {
    this.modals.close(null);
  }

  public saveDisabled() {
    let durationPass = this.durationChoice === 0 ? true : this.weeksInput > 0;
    return (!this.nameInput || !this.descriptionInput || !this.focusInput || this.startDayInput < 0 || !durationPass);
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
