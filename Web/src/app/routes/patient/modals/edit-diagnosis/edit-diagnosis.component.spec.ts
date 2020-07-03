import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditDiagnosisComponent } from './edit-diagnosis.component';

describe('EditDiagnosisComponent', () => {
  let component: EditDiagnosisComponent;
  let fixture: ComponentFixture<EditDiagnosisComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditDiagnosisComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditDiagnosisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
