"""
LLMクライアント統合インターフェース
OpenAI, Gemini, Anthropicをサポート
複数プロバイダーの自動選択・フォールバック機能付き
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Tuple
import os
import sys


def safe_print(message: str):
    """
    Windowsコンソールでも安全にメッセージを表示するヘルパー関数
    絵文字が表示できない場合は代替文字を使用
    """
    try:
        print(message)
    except UnicodeEncodeError:
        # 絵文字を代替テキストに置換
        replacements = {
            '💰': '[$]',
            '✅': '[+]',
            '⚠️': '[!]',
            '❌': '[x]'
        }
        safe_message = message
        for emoji, replacement in replacements.items():
            safe_message = safe_message.replace(emoji, replacement)
        print(safe_message)


class LLMClient(ABC):
    """LLMクライアントの抽象基底クラス"""

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        """
        テキストを生成

        Args:
            system_prompt: システムプロンプト
            user_prompt: ユーザープロンプト
            temperature: 温度パラメータ (0.0-1.0)
            max_tokens: 最大トークン数

        Returns:
            生成されたテキスト、失敗時はNone
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """プロバイダー名を取得"""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """モデル名を取得"""
        pass

    @abstractmethod
    def get_cost_per_1m_tokens(self) -> Tuple[float, float]:
        """
        1Mトークンあたりのコストを取得

        Returns:
            (入力コスト, 出力コスト) のタプル (USD)
        """
        pass


class OpenAIClient(LLMClient):
    """OpenAI APIクライアント"""

    # モデルごとの料金 (USD per 1M tokens)
    PRICING = {
        "gpt-5-nano": (0.50, 2.00),
        "gpt-4-turbo": (10.00, 30.00),
    }

    def __init__(self, api_key: str, model: str = "gpt-5-nano"):
        """
        Args:
            api_key: OpenAI APIキー
            model: モデル名 (gpt-5-nano, gpt-4-turbo等)
        """
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        try:
            params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_completion_tokens": max_tokens
            }

            # gpt-5-nanoはtemperatureをサポートしない
            if not ("gpt-5" in self.model.lower() and "nano" in self.model.lower()):
                params["temperature"] = temperature

            response = self.client.chat.completions.create(**params)
            return response.choices[0].message.content

        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None

    def get_provider_name(self) -> str:
        return "OpenAI"

    def get_model_name(self) -> str:
        return self.model

    def get_cost_per_1m_tokens(self) -> Tuple[float, float]:
        """1Mトークンあたりのコストを取得"""
        return self.PRICING.get(self.model, (10.0, 30.0))  # デフォルトはgpt-4-turbo


class GeminiClient(LLMClient):
    """Google Gemini APIクライアント"""

    # モデルごとの料金 (USD per 1M tokens)
    PRICING = {
        "gemini-2.5-flash": (0.075, 0.30),
        "gemini-2.0-flash": (0.10, 0.40),
    }

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        """
        Args:
            api_key: Google AI Studio APIキー
            model: モデル名 (gemini-2.5-flash, gemini-2.0-flash等)
        """
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.model_name = model
        self.model = genai.GenerativeModel(model)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        try:
            # Gemini APIでは、system_instructionをモデル初期化時に設定可能
            # ただし、ここでは実行時に設定するため、プロンプトに統合
            combined_prompt = f"{system_prompt}\n\n{user_prompt}"

            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }

            response = self.model.generate_content(
                combined_prompt,
                generation_config=generation_config
            )

            return response.text

        except Exception as e:
            print(f"Gemini API error: {e}")
            return None

    def get_provider_name(self) -> str:
        return "Google Gemini"

    def get_model_name(self) -> str:
        return self.model_name

    def get_cost_per_1m_tokens(self) -> Tuple[float, float]:
        """1Mトークンあたりのコストを取得"""
        return self.PRICING.get(self.model_name, (0.10, 0.40))  # デフォルトはgemini-2.0-flash


class AnthropicClient(LLMClient):
    """Anthropic Claude APIクライアント"""

    # モデルごとの料金 (USD per 1M tokens)
    PRICING = {
        "claude-4.5-haiku": (0.25, 1.25),
        "claude-3.5-sonnet": (3.00, 15.00),
    }

    def __init__(self, api_key: str, model: str = "claude-4.5-haiku"):
        """
        Args:
            api_key: Anthropic APIキー
            model: モデル名 (claude-4.5-haiku, claude-3.5-sonnet等)
        """
        from anthropic import Anthropic
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            return response.content[0].text

        except Exception as e:
            print(f"Anthropic API error: {e}")
            return None

    def get_provider_name(self) -> str:
        return "Anthropic"

    def get_model_name(self) -> str:
        return self.model

    def get_cost_per_1m_tokens(self) -> Tuple[float, float]:
        """1Mトークンあたりのコストを取得"""
        return self.PRICING.get(self.model, (3.00, 15.00))  # デフォルトはclaude-3.5-sonnet


class MultiProviderLLMClient(LLMClient):
    """
    複数のLLMプロバイダーを管理し、コスト最適化とフォールバックを行うクライアント
    """

    def __init__(self, clients: List[LLMClient]):
        """
        Args:
            clients: LLMクライアントのリスト
        """
        if not clients:
            raise ValueError("At least one client is required")

        # コストの安い順にソート（入力+出力の平均コスト）
        self.clients = sorted(
            clients,
            key=lambda c: sum(c.get_cost_per_1m_tokens()) / 2
        )
        self.current_client_index = 0

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        """
        複数のプロバイダーを試して生成
        最安のプロバイダーから順に試し、失敗したら次へフォールバック
        """
        last_error = None

        for i, client in enumerate(self.clients):
            try:
                if i == 0:
                    safe_print(f"💰 Using cheapest provider: {client.get_provider_name()} {client.get_model_name()}")
                else:
                    safe_print(f"⚠️  Fallback to: {client.get_provider_name()} {client.get_model_name()}")

                result = client.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                if result is not None:
                    self.current_client_index = i
                    cost = client.get_cost_per_1m_tokens()
                    safe_print(f"✅ Success! Cost: ${cost[0]:.3f}/${cost[1]:.3f} per 1M tokens (input/output)")
                    return result

            except Exception as e:
                last_error = e
                safe_print(f"❌ {client.get_provider_name()} failed: {e}")
                continue

        safe_print(f"❌ All providers failed. Last error: {last_error}")
        return None

    def get_provider_name(self) -> str:
        """現在使用中のプロバイダー名を取得"""
        if self.current_client_index < len(self.clients):
            return self.clients[self.current_client_index].get_provider_name()
        return "MultiProvider"

    def get_model_name(self) -> str:
        """現在使用中のモデル名を取得"""
        if self.current_client_index < len(self.clients):
            return self.clients[self.current_client_index].get_model_name()
        return "Multiple"

    def get_cost_per_1m_tokens(self) -> Tuple[float, float]:
        """現在使用中のプロバイダーのコストを取得"""
        if self.current_client_index < len(self.clients):
            return self.clients[self.current_client_index].get_cost_per_1m_tokens()
        # 平均コストを返す
        avg_input = sum(c.get_cost_per_1m_tokens()[0] for c in self.clients) / len(self.clients)
        avg_output = sum(c.get_cost_per_1m_tokens()[1] for c in self.clients) / len(self.clients)
        return (avg_input, avg_output)

    def get_available_providers(self) -> List[str]:
        """利用可能なプロバイダーのリストを取得（コストの安い順）"""
        return [
            f"{c.get_provider_name()} {c.get_model_name()} (${sum(c.get_cost_per_1m_tokens())/2:.3f}/1M avg)"
            for c in self.clients
        ]


def create_llm_client(
    provider: str,
    model: str,
    api_key: Optional[str] = None
) -> Optional[LLMClient]:
    """
    LLMクライアントを作成

    Args:
        provider: プロバイダー名 ("openai", "gemini", "google", "anthropic")
        model: モデル名
        api_key: APIキー（指定しない場合は環境変数から取得）

    Returns:
        LLMClientインスタンス、失敗時はNone
    """
    provider = provider.lower()

    # "google" を "gemini" のエイリアスとして扱う
    if provider == "google":
        provider = "gemini"

    # APIキーを環境変数から取得（指定されていない場合）
    if api_key is None:
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
        elif provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        elif provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print(f"Warning: No API key found for {provider}")
        return None

    try:
        if provider == "openai":
            return OpenAIClient(api_key=api_key, model=model)
        elif provider == "gemini":
            return GeminiClient(api_key=api_key, model=model)
        elif provider == "anthropic":
            return AnthropicClient(api_key=api_key, model=model)
        else:
            print(f"Unknown provider: {provider}")
            return None

    except Exception as e:
        print(f"Failed to create LLM client for {provider}: {e}")
        return None


def create_multi_provider_client(
    auto_detect: bool = True,
    providers: Optional[List[Dict[str, str]]] = None
) -> Optional[LLMClient]:
    """
    複数のプロバイダーをサポートするクライアントを作成
    環境変数からAPIキーを自動検出し、コストの安い順に使用

    Args:
        auto_detect: Trueの場合、環境変数から自動検出
        providers: プロバイダー設定のリスト [{"provider": "gemini", "model": "gemini-2.5-flash"}, ...]

    Returns:
        MultiProviderLLMClientインスタンス、失敗時はNone
    """
    clients = []

    if auto_detect:
        # 環境変数から自動検出
        # Gemini (最安)
        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if gemini_key:
            try:
                client = GeminiClient(api_key=gemini_key, model="gemini-2.5-flash")
                clients.append(client)
                safe_print(f"✅ Detected: Google Gemini (gemini-2.5-flash)")
            except Exception as e:
                safe_print(f"⚠️  Failed to initialize Gemini: {e}")

        # Anthropic (コスパ良)
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            try:
                client = AnthropicClient(api_key=anthropic_key, model="claude-4.5-haiku")
                clients.append(client)
                safe_print(f"✅ Detected: Anthropic Claude (claude-4.5-haiku)")
            except Exception as e:
                safe_print(f"⚠️  Failed to initialize Anthropic: {e}")

        # OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                client = OpenAIClient(api_key=openai_key, model="gpt-5-nano")
                clients.append(client)
                safe_print(f"✅ Detected: OpenAI (gpt-5-nano)")
            except Exception as e:
                safe_print(f"⚠️  Failed to initialize OpenAI: {e}")

    elif providers:
        # 指定されたプロバイダーを使用
        for config in providers:
            provider = config.get("provider", "").lower()
            model = config.get("model", "")
            client = create_llm_client(provider, model)
            if client:
                clients.append(client)

    if not clients:
        safe_print("❌ No LLM providers available")
        return None

    return MultiProviderLLMClient(clients)
