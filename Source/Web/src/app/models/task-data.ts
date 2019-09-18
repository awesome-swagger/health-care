
export interface ITaskData {
  checkIns: Array<{ patient: string, time: string }>,
  length: number,
  tasks: Array<{ patient: string, tasks: number }>
}
