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
  public startDayInput = '';
  public durationChoice = 0;
  public weeksInput = 1;

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
      this.weeksInput = g.duration_weeks !== -1 ? g.duration_weeks : null;
    }
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
    this.modals.close({
      name: this.nameInput,
      description: this.descriptionInput,
      focus: this.focusInput,
      start_on_day: this.startDayInput,
      duration_weeks: durationWeeks,
    });
  }
}
