import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CarePlanConsentComponent } from './care-plan-consent.component';

describe('CarePlanConsentComponent', () => {
  let component: CarePlanConsentComponent;
  let fixture: ComponentFixture<CarePlanConsentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CarePlanConsentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CarePlanConsentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
