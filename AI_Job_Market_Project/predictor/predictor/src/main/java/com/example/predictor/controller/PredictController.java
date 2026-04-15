package com.example.predictor.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

@RestController
@RequestMapping("/api")
public class PredictController {

	@GetMapping("/predict")
    public String predict(@RequestParam int year) {

        String url = "http://127.0.0.1:5000/predict?year=" + year;

        RestTemplate restTemplate = new RestTemplate();

        String response = restTemplate.getForObject(url, String.class);

        return response;
    }
}
