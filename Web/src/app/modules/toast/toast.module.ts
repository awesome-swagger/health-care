import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RouterModule } from '@angular/router';

import { ToastComponent } from './toast.component';
import { ToastService } from './toast.service';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    BrowserAnimationsModule,
  ],
  declarations: [ToastComponent],
  providers: [ToastService],
  exports: [
    ToastComponent,
  ]
})
export class ToastModule { }
