import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReassignBillingPractitionerComponent } from './reassign-billing-practitioner.component';

describe('ReassignBillingPractitionerComponent', () => {
  let component: ReassignBillingPractitionerComponent;
  let fixture: ComponentFixture<ReassignBillingPractitionerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ReassignBillingPractitionerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ReassignBillingPractitionerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
