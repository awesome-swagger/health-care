import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'timeTransform'
})
export class TimeTransformPipe implements PipeTransform {

  transform(value: any, args?: any): any {
    let time = value.split(':');
    let temp:any = new Date();
    temp.setHours(time[0]);
    temp.setMinutes(time[1]);
    return temp;

  }

}
