import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-create-stream',
  templateUrl: './create-stream.component.html',
  styleUrls: ['./create-stream.component.scss'],
})
export class CreateStreamComponent implements OnInit {

  public data = null;

  public tooltipCMS0Open
  public tooltipCMS1Open
  public deleteM0;
  public deleteM1;
  public deleteM2;
  public showAddMessageForm;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
