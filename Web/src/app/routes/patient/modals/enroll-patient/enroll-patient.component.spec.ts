import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EnrollPatientComponent } from './enroll-patient.component';

describe('EnrollPatientComponent', () => {
  let component: EnrollPatientComponent;
  let fixture: ComponentFixture<EnrollPatientComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EnrollPatientComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EnrollPatientComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
