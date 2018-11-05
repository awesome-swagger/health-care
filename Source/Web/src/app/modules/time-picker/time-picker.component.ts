import { Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
import { PopoverOptions } from '../popover';

@Component({
  selector: 'app-time-picker',
  templateUrl: './time-picker.component.html',
  styleUrls: ['./time-picker.component.scss']
})
export class TimePickerComponent implements OnInit {

  private _hourValue = 12;
  private _minuteValue = 0;
  private _periodValue = 'am';

  public timePickerVisible = false;

  public popoverOptions: PopoverOptions = {
    width: '200px',
  };

  public value = '';

  @Input() disabled: boolean = false;
  @Input() startingValue: string;
  @Input() militaryTime: boolean = false;


  @Output()
  public valueChange = new EventEmitter();

  constructor() { }

  public ngOnInit() {
    this.updateTime();
  }

  public incrementHour() {
    if (this.hourValue >= 12) {
      this.hourValue = 1;
    } else {
      this.hourValue++;
    }
  }

  public decrementHour() {
    if (this.hourValue <= 1) {
      this.hourValue = 12;
    } else {
      this.hourValue--;
    }
  }

  public incrementMinute() {
    if (this.minuteValue >= 59) {
      this.minuteValue = 0;
    } else {
      this.minuteValue++;
    }
  }

  public decrementMinute() {
    if (this.minuteValue <= 0) {
      this.minuteValue = 59;
    } else {
      this.minuteValue--;
    }
  }

  public incrementPeriod() {
    if (this.periodValue === 'am') {
      this.periodValue = 'pm';
    } else {
      this.periodValue = 'am';
    }
  }

  public decrementPeriod() {
    this.incrementPeriod();
  }

  public zeroPad(value) {
    if (parseInt(value) < 10) {
      return `0${value}`;
    } else {
      return `${value}`;
    }
  }

  public openTimePicker() {
    if (this.disabled) return;
    this.timePickerVisible = true;
  }

  public to24Hour() {
    let actualHour = this.hourValue;
    if (this.periodValue === 'pm' && this.hourValue < 12) {
      actualHour = this.hourValue + 12;
    } else if (this.periodValue === 'am' && this.hourValue == 12) {
      actualHour = this.hourValue - 12;
    }
    return `${this.zeroPad(actualHour)}:${this.zeroPad(this.minuteValue)}:00`
  }

  public updateTime() {
    this.value = this.militaryTime ? this.to24Hour() : `${this.zeroPad(this.hourValue)}:${this.zeroPad(this.minuteValue)} ${this.periodValue}`;
    this.valueChange.emit(this.to24Hour());
  }

  public get hourValue() {
    return this._hourValue;
  }

  public set hourValue(value) {
    this._hourValue = value;
    this.updateTime();
  }

  public get minuteValue() {
    return this._minuteValue;
  }

  public set minuteValue(value) {
    this._minuteValue = value;
    this.updateTime();
  }

  public get periodValue() {
    return this._periodValue;
  }

  public set periodValue(value) {
    this._periodValue = value;
    this.updateTime();
  }
}
