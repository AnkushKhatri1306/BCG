import { Injectable } from '@angular/core';
import {map} from 'rxjs/operators';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class UserpolicyService {


  constructor(private http: HttpClient) { }
  baseUrl: string = "http://127.0.0.1:9001";
  
  getInsurancePolicyList(paramsData: any){
    return this.http.get<any>(this.baseUrl + '/policy/home/list/', {
      params: new HttpParams().append('page_size', paramsData.page_size).append('page_number', 
      paramsData.page_number).append('search_id', paramsData.search_id)
    })
    .pipe(map((resp) => {
      return resp;
    }));
  }

  savePolicyData(data:any){
    return this.http.post<any>(this.baseUrl + "/policy/home/save_policy/", data, {
      // headers: new HttpHeaders().set('Authorization', '')
    })
  }

  getInsurancePolicyOptions(){
    return this.http.get<any>(this.baseUrl + '/policy/home/options/', {
    })
    .pipe(map((resp) => {
      return resp;
    }));
  }

  getInsurancePolicy(policy_id: any){
    return this.http.get<any>(this.baseUrl + '/policy/home/get_policy/', {
      params: new HttpParams().append('policy_id', policy_id)
    })
    .pipe(map((resp) => {
      return resp;
    }));
  }



}
