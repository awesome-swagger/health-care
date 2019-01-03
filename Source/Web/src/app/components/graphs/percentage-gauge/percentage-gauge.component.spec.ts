import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PercentageGaugeComponent } from './percentage-gauge.component';

describe('PercentageGaugeComponent', () => {
  let component: PercentageGaugeComponent;
  let fixture: ComponentFixture<PercentageGaugeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PercentageGaugeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PercentageGaugeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
