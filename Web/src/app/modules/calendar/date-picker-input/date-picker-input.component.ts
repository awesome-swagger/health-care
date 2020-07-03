import { Component, OnInit, Input } from '@angular/core';
import * as moment from 'moment';

@Component({
  selector: 'app-date-picker-input',
  templateUrl: './date-picker-input.component.html',
  styleUrls: ['./date-picker-input.component.scss']
})
export class DatePickerInputComponent implements OnInit {

  @Input() top: Boolean;

  constructor() { }

  public data = null;
  public datePickerOpen = false;
  public selectedDate = moment();

  ngOnInit() {
  }

  openDatePicker() {
    this.datePickerOpen = true;
  }

  closeDatePicker() {
    this.datePickerOpen = false;
  }

  get formattedDate() {
    return moment(this.selectedDate).format('MM/DD/YYYY');
  }

  set formattedDate(date) {
    this.selectedDate = moment(date);
  }
}
