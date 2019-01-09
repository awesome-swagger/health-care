import { Component, OnDestroy, OnInit } from '@angular/core';

@Component({
  selector: 'app-billing',
  templateUrl: './billing.component.html',
  styleUrls: ['./billing.component.scss'],
})
export class BillingComponent implements OnDestroy, OnInit {

  constructor() { }

  public tooltip1Open;
  public multi1Open;
  public multi2Open;
  public dropOpen;
  public tooltip2Open;
  public accord1Open;
  public isBilled1;
  public accordInner1Open;
  public isBilled2;
  public accordInner2Open;

  public ngOnInit() { }

  public ngOnDestroy() { }
}
