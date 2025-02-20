import { useEffect, useState } from 'react';
import './App.css';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';

function App() {
  const [feedback, setFeedback] = useState('gerar_teste');
  const [showFeedback, setShowFeedback] = useState(true);
  const [codeResponse, setCodeResponse] = useState('');
  const [codeInput, setCodeInput] = useState('');
  const feedbackDefault = {
    "code_id": 0,
    "feedback": null
  }
  const [userFeedback, setUserFeedback] = useState(feedbackDefault);
  const [showThanks, setShowThanks] = useState(false);
  const [feedbackMessage, setFeedbackMessage] = useState('');
  const [language, setLanguage] = useState('plaintext');


  const handleGenerateTest = async () => {
    setCodeResponse("Criando seu teste...");
    setFeedback('gerar_teste')
    setUserFeedback(feedbackDefault)
    setShowThanks(false)
    setFeedbackMessage('')
    setLanguage('plaintext')
    try {
      const response = await fetch('http://127.0.0.1:5000/api/code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: codeInput }),
      });

      if (!response.ok) {
        throw new Error('Erro ao gerar resposta');
      }

      const data = await response.json();
      setCodeResponse(data.testing);
      setFeedback('feedback');
      setUserFeedback(prevState => ({
        ...prevState,
        code_id: data.id_response
      }));
    }
    catch (error) {
      setCodeResponse('Erro ao processar a solicitação.');
    }
  };
  const handleFeedback = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userFeedback),
      });

      if (!response.ok) {
        throw new Error('Erro ao gerar resposta');
      }

      setShowThanks(true);
      setFeedbackMessage('Obrigada pelo feedback.');
    } catch (error) {
      setShowThanks(true);
      setFeedbackMessage('Erro ao processar a solicitação.');
    }
  };
  useEffect(() => {
    if (userFeedback.feedback != null) {
      handleFeedback();
    }
  }, [userFeedback]);
  useEffect(() => {
    const detectLanguage = (code) => {
      const match = code.match(/```(\w+)/);
      const cleanCode = codeResponse.replace(/```(\w+)\n/g, '').replace(/```$/, '');
      setCodeResponse(cleanCode)
      return match ? match[1] : 'plaintext';
    };
    if (language == 'plaintext') {
      setLanguage(detectLanguage(codeResponse))
    }
  }, [codeResponse]);

  return (
    <>
      <div className='page'>
        <section className="code">
          <textarea
            type="text"
            className="code-input"
            placeholder="Digite seu código."
            value={codeInput}
            onChange={(e) => setCodeInput(e.target.value)}
          />
        </section>

        <section className='test'>
          <div className={feedback}>
            <button className='gerar' onClick={handleGenerateTest}>
              Gerar {feedback === "feedback" && 'Novamente'}
            </button>

            {feedback === "feedback" && showFeedback && (
              <div className='botoes'>
                <button className='feedbacks' onClick={() => {
                  setUserFeedback(prevState => ({
                    ...prevState,
                    feedback: true
                  }));
                  setShowFeedback(false)
                }}>✔</button>
                <button className='feedbacks' onClick={() => {
                  setUserFeedback(prevState => ({
                    ...prevState,
                    feedback: false
                  }));
                  setShowFeedback(false)
                }}>✖</button>
              </div>
            )}
          </div>

          <div className='llm'>
            <SyntaxHighlighter language={language}>
              {codeResponse}
            </SyntaxHighlighter>
          </div>
        </section>
      </div>
      {showThanks && <div className='modal'>
        <div className='message'>
          <button className='close' onClick={() => setShowThanks(false)}>X</button>
          {feedbackMessage}
        </div>
      </div>}
    </>


  );
}

export default App;
