import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PopoverModule } from '../popover';

import { TimePickerComponent } from './time-picker.component';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    PopoverModule,
  ],
  declarations: [TimePickerComponent],
  providers: [],
  exports: [TimePickerComponent],
})
export class TimePickerModule { }
