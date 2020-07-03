import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditProcedureComponent } from './edit-procedure.component';

describe('EditProcedureComponent', () => {
  let component: EditProcedureComponent;
  let fixture: ComponentFixture<EditProcedureComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditProcedureComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditProcedureComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
