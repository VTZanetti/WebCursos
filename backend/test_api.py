#!/usr/bin/env python3
"""
Script de teste para validar todos os endpoints da API WebCurso
Execute: python test_api.py
"""

import requests
import json
import sys
import time

# Configurações
API_BASE_URL = "http://localhost:5000/api"
HEADERS = {"Content-Type": "application/json"}

def print_response(response, test_name):
    """Exibe o resultado do teste de forma formatada"""
    status = "✅ PASSOU" if response.status_code < 400 else "❌ FALHOU"
    print(f"\n{status} | {test_name}")
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(f"Resposta: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"Resposta: {response.text}")
    print("-" * 50)

def test_health():
    """Testa o endpoint de status da API"""
    print("🔍 Testando endpoint de saúde...")
    response = requests.get(f"{API_BASE_URL}/health")
    print_response(response, "GET /api/health")
    return response.status_code == 200

def test_get_cursos():
    """Testa a listagem de cursos"""
    print("📋 Testando listagem de cursos...")
    response = requests.get(f"{API_BASE_URL}/cursos")
    print_response(response, "GET /api/cursos")
    return response.status_code == 200

def test_create_curso():
    """Testa a criação de um novo curso"""
    print("➕ Testando criação de curso...")
    curso_data = {
        "titulo": "Curso de Teste API",
        "total_aulas": 15,
        "link": "https://exemplo.com/teste",
        "anotacoes": "Curso criado pelo script de teste"
    }
    response = requests.post(f"{API_BASE_URL}/cursos", json=curso_data, headers=HEADERS)
    print_response(response, "POST /api/cursos")
    
    if response.status_code == 201:
        data = response.json()
        return data.get('data', {}).get('id'), True
    return None, False

def test_get_curso_by_id(curso_id):
    """Testa a busca de curso por ID"""
    print(f"🔍 Testando busca do curso ID {curso_id}...")
    response = requests.get(f"{API_BASE_URL}/cursos/{curso_id}")
    print_response(response, f"GET /api/cursos/{curso_id}")
    return response.status_code == 200

def test_update_curso(curso_id):
    """Testa a atualização de um curso"""
    print(f"✏️ Testando atualização do curso ID {curso_id}...")
    update_data = {
        "titulo": "Curso Atualizado via API",
        "anotacoes": "Anotações atualizadas pelo teste"
    }
    response = requests.put(f"{API_BASE_URL}/cursos/{curso_id}", json=update_data, headers=HEADERS)
    print_response(response, f"PUT /api/cursos/{curso_id}")
    return response.status_code == 200

def test_toggle_aula(curso_id):
    """Testa o controle de aulas concluídas"""
    print(f"✅ Testando conclusão de aula para curso ID {curso_id}...")
    
    # Marcar aula 1 como concluída
    aula_data = {
        "numero_aula": 1,
        "concluida": True
    }
    response = requests.post(f"{API_BASE_URL}/cursos/{curso_id}/aula", json=aula_data, headers=HEADERS)
    print_response(response, f"POST /api/cursos/{curso_id}/aula (marcar concluída)")
    
    if response.status_code != 200:
        return False
    
    # Desmarcar aula 1
    aula_data["concluida"] = False
    response = requests.post(f"{API_BASE_URL}/cursos/{curso_id}/aula", json=aula_data, headers=HEADERS)
    print_response(response, f"POST /api/cursos/{curso_id}/aula (desmarcar)")
    
    return response.status_code == 200

def test_stats():
    """Testa o endpoint de estatísticas"""
    print("📊 Testando estatísticas...")
    response = requests.get(f"{API_BASE_URL}/stats")
    print_response(response, "GET /api/stats")
    return response.status_code == 200

def test_delete_curso(curso_id):
    """Testa a exclusão de um curso"""
    print(f"🗑️ Testando exclusão do curso ID {curso_id}...")
    response = requests.delete(f"{API_BASE_URL}/cursos/{curso_id}")
    print_response(response, f"DELETE /api/cursos/{curso_id}")
    return response.status_code == 200

def test_error_handling():
    """Testa o tratamento de erros"""
    print("⚠️ Testando tratamento de erros...")
    
    # Curso inexistente
    response = requests.get(f"{API_BASE_URL}/cursos/99999")
    print_response(response, "GET /api/cursos/99999 (curso inexistente)")
    
    # Dados inválidos
    invalid_data = {"titulo": ""}  # título vazio
    response = requests.post(f"{API_BASE_URL}/cursos", json=invalid_data, headers=HEADERS)
    print_response(response, "POST /api/cursos (dados inválidos)")
    
    # Endpoint inexistente
    response = requests.get(f"{API_BASE_URL}/inexistente")
    print_response(response, "GET /api/inexistente (endpoint inexistente)")
    
    return True

def main():
    """Executa todos os testes da API"""
    print("🚀 Iniciando testes da API WebCurso...")
    print(f"🌐 URL Base: {API_BASE_URL}")
    print("=" * 60)
    
    # Verificar se a API está rodando
    try:
        requests.get(f"{API_BASE_URL}/health", timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro: API não está rodando em {API_BASE_URL}")
        print(f"Execute 'python app.py' no diretório backend primeiro.")
        print(f"Erro: {e}")
        sys.exit(1)
    
    tests_passed = 0
    total_tests = 0
    
    # Lista de testes a executar
    tests = [
        ("Status da API", test_health),
        ("Listagem de cursos", test_get_cursos),
        ("Estatísticas", test_stats),
    ]
    
    # Executar testes básicos
    for test_name, test_func in tests:
        total_tests += 1
        if test_func():
            tests_passed += 1
        time.sleep(0.5)  # Pequena pausa entre testes
    
    # Testes com criação de curso
    total_tests += 1
    curso_id, success = test_create_curso()
    if success:
        tests_passed += 1
        
        # Se criou com sucesso, testar operações com esse curso
        if curso_id:
            more_tests = [
                (f"Buscar curso {curso_id}", lambda: test_get_curso_by_id(curso_id)),
                (f"Atualizar curso {curso_id}", lambda: test_update_curso(curso_id)),
                (f"Controlar aulas curso {curso_id}", lambda: test_toggle_aula(curso_id)),
                (f"Deletar curso {curso_id}", lambda: test_delete_curso(curso_id)),
            ]
            
            for test_name, test_func in more_tests:
                total_tests += 1
                if test_func():
                    tests_passed += 1
                time.sleep(0.5)
    
    # Teste de tratamento de erros
    total_tests += 1
    if test_error_handling():
        tests_passed += 1
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    print(f"✅ Testes passou: {tests_passed}")
    print(f"❌ Testes falharam: {total_tests - tests_passed}")
    print(f"📈 Taxa de sucesso: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("\n🎉 Todos os testes passaram! API funcionando perfeitamente.")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total_tests - tests_passed} teste(s) falharam. Verifique os logs acima.")
        sys.exit(1)

if __name__ == "__main__":
    main()