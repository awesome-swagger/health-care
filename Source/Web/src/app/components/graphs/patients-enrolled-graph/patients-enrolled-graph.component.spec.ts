import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PatientsEnrolledGraphComponent } from './patients-enrolled-graph.component';

describe('PatientsEnrolledGraphComponent', () => {
  let component: PatientsEnrolledGraphComponent;
  let fixture: ComponentFixture<PatientsEnrolledGraphComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PatientsEnrolledGraphComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PatientsEnrolledGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
