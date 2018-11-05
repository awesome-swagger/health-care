import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { AppModule } from '../../../app.module';
import { InactivePatientsComponent } from './inactive.component';

describe('InactivePatientsComponent', () => {
  let component: InactivePatientsComponent;
  let fixture: ComponentFixture<InactivePatientsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        AppModule
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InactivePatientsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
