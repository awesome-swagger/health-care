import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-reminder-email',
  templateUrl: './reminder-email.component.html',
  styleUrls: ['./reminder-email.component.scss'],
})
export class ReminderEmailComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
