import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditBillingPractitionerComponent } from './edit-billing-practitioner.component';

describe('EditBillingPractitionerComponent', () => {
  let component: EditBillingPractitionerComponent;
  let fixture: ComponentFixture<EditBillingPractitionerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditBillingPractitionerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditBillingPractitionerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
