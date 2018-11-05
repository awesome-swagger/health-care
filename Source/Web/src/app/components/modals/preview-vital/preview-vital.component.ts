import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-preview-vital',
  templateUrl: './preview-vital.component.html',
  styleUrls: ['./preview-vital.component.scss'],
})
export class PreviewVitalComponent implements OnInit {

  public data = null;

  constructor() {

  }

  public ngOnInit() {
    console.log(this.data);
  }
}
