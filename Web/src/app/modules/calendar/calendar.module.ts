import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { DatePickerComponent } from './date-picker/date-picker.component';
import { DateRangeComponent } from './date-range/date-range.component';
import { PopoverModule } from '../popover';
import { DatePickerInputComponent } from './date-picker-input/date-picker-input.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    PopoverModule,
  ],
  declarations: [
    DatePickerComponent,
    DateRangeComponent,
    DatePickerInputComponent,
  ],
  providers: [],
  exports: [
    DatePickerComponent,
    DateRangeComponent,
    DatePickerInputComponent,
  ],
})
export class CalendarModule { }
