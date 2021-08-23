# Tutorial: How to build an ML backend for Ink

## Purpose
This goal of this tutorial is to describe, how to build a fast prototype for a REST API to serve an experimental 
deep learning system for digital ink utilizing Wacom's Universal Ink Model.

## Train a model
In order to train a machine learning  model, you can pick your favorite framework:

- **Keras** - [https://keras.io/](https://keras.io/)
- **Tensorflow** - [https://www.tensorflow.org/](https://www.tensorflow.org/)
- **PyTorch** - [https://pytorch.org/](https://pytorch.org/)
- **Scikit learn** - [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)
- ...

The project `model-trainer` contains a sample the extract sensor data. 

The projects contains a folder `models` where you should store the trained models.

## FastAPI
FastAPI is an easy-to-use framework to build Python REST APIs (micro-services).

## Deployment
The sample service is packaged as a Docker container, thus it can be deployed in several cloud infrastructures, for instance:

- Amazon's AWS
- Microsoft Azure
- Digital Ocean 
- Heroku 

###  Heroku
Exemplary, we will use Heroku deploy.

**1. Step**: 
Create a Heroku account and configure your backend

**2. Step**: 
Log into your container registry.

```
$ heroku container login
```

**3. Step**: 
Build docker image and push it to Heroku registry.

```
$ heroku container:push web --app <APP-NAME>
```

**3. Step**: 
Build docker image and push it to Heroku registry.

```
$ heroku container:release web --app <APP-NAME>
```

**Access logging**: 
Build docker image and push it to Heroku registry.

```
$ heroku logs --tail --app <APP-NAME>
```

## Universal Ink Library
You can find more samples on how to use Wacom's Universal Ink Library [here](https://github.com/Wacom-Developer/universal-ink-library)

## Documentation
For further details on using the SDK see [WILL SDK for ink documentation](http://developer-docs.wacom.com/sdk-for-ink/)

The API Reference is available directly in the downloaded SDK.

## Support
If you experience issues with the technology components, please see related [FAQs](http://developer-docs.wacom.com/faqs)

For further support file a ticket in our **Developer Support Portal** described here: [Request Support](http://developer-docs.wacom.com/faqs/docs/q-support/support)

## Developer Community
Join our developer community:

- [LinkedIn - Wacom for Developers](https://www.linkedin.com/company/wacom-for-developers/)
- [Twitter - Wacom for Developers](https://twitter.com/Wacomdevelopers)

## License
This sample code is licensed under the [MIT License](https://choosealicense.com/licenses/mit/)
