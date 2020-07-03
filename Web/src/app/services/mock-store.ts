export class MockStore<T> {

  private objects: T[] = [];

  constructor() { }

  public create(payload: any) {
    let objIds = this.objects.map((obj: any) => { return obj.id; });
    let highestId = 0;
    if (objIds.length !== 0) {
      objIds.forEach((id) => {
        if (id > highestId) {
          highestId = id;
        }
      });
    }
    payload.id = highestId + 1;
    this.objects.push(payload);
    let idx = this.objects.findIndex((obj: any) => { return obj.id === payload.id });
    return this.objects[idx];
  }

  public read(id) {
    id = parseInt(id);
    let match = this.objects.find((obj: any) => { return obj.id === id; });
    return match;
  }

  public readList() {
    return this.objects;
  }

  public update(id: string, payload: any) {
    let idx = this.objects.findIndex((obj: any) => { return obj.id === id });
    this.objects[idx] = Object.assign({}, this.objects[idx], payload);
    return this.objects[idx];
  }

  public destroy(id: string) {
    let idx = this.objects.findIndex((obj: any) => { return obj.id === id });
    this.objects = this.objects.splice(idx, 1);
    return null;
  }
}
